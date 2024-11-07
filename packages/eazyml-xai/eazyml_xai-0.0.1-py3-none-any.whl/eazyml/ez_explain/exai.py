from sklearn.preprocessing import StandardScaler
from .exai_main import get_random_train_data
from .exai_main import get_pdf_data
from .exai_main import get_parallel_explanations_pool
from .exai_main import get_exai_explanations
from .exai_utils_explain import DotDict
import traceback
import numpy as np
from concurrent.futures import ProcessPoolExecutor as Pool


class ParallelWrapper(object):
    def __init__(self):
        self.dummy = 0
    def __call__(self, arg_item):
        return get_parallel_explanations_pool(arg_item)


def get_explanations_all_records(
    train_data, outcome,
    mode, test_point,
    test_point_pred,
    raw_test_point,
    extra_info
    ): 
    g = DotDict(extra_info["g"])
    arg_items = []
    t_data = None
    if not g.ONLY_PERTURBED_POINTS or g.LIME_FOR_CLASSIF or g.LIME_FOR_REGR:
        t_data = train_data
    results = []
    for item in range(len(extra_info['rec'])):
        extra_info[g.TEST_PT_PRED] = raw_test_point[outcome].iloc[item]
        # "Predicted " + outcome].iloc[item]
        raw_test_point_rec = raw_test_point.iloc[item]
        #arg_items.append((t_data, outcome,
        #                  mode,
        #                  test_point[item].reshape(1, -1),
        #                  raw_test_point_rec,
        #                  extra_info.copy())
        #                )
        res = get_exai_explanations(
            t_data, outcome, mode,
            test_point[item].reshape(1, -1), raw_test_point_rec,
            extra_info.copy())
        results.append(res)
    #with Pool(g.NUMBER_OF_PROCESSES) as p:
    #    results = p.map(ParallelWrapper(), arg_items)
    response = []
    for item, rec, result in zip(range(len(extra_info['rec'])),
        extra_info['rec'], results):
        res = dict()
        res["record_number"] = rec
        res["prediction"] = result[2]
        res["explanation"] = result[1]
        res["explainability_score"] = result[3]
        res["local_importance"] = result[0]
        if "Confidence Score" in raw_test_point.columns:
            res["confidence_score"] = raw_test_point[
                "Confidence Score"].iloc[item]
        response.append(res)
    return response


def get_explainable_ai(input_object):
    try:
        # extracting parameters
        train_data = input_object['train_data']
        test_data_processed = input_object['test_data']
        outcome = input_object['outcome']
        g_orig = input_object['g']
        g = DotDict(g_orig)

        extra_info = {}
        extra_info['rec'] = input_object['record_numbers']
        ind = [i-1 for i in extra_info['rec']]
        raw_test_point_processed = test_data_processed.iloc[ind]
        tr_cols = train_data.columns.values.tolist()
        if outcome in tr_cols:
            tr_cols.remove(outcome)
        test_point = raw_test_point_processed[tr_cols].values.astype('float64')
        test_point = test_point.reshape(len(extra_info['rec']),-1)
        extra_info[g.RULE_LIME] = {'columns': tr_cols}
        extra_info[g.FEATURES_SELECTED] = tr_cols
        '''
        extra_info[g.DATA_TYPE] = pd.DataFrame.from_dict(input_object[g.DATA_TYPE])
        extra_info[g.STAT] = pd.DataFrame.from_dict(input_object[g.STAT])
        extra_info[g.LIME_OBJECT] = input_object[g.LIME_OBJECT]
        extra_info[g.MODELLING_URL] = ex_ai_dict[g.MODELLING_URL]
        '''
        if input_object['scaler'] is not None:
            extra_info[g.SCALER] = input_object['scaler']
        extra_info[g.MODEL_PATH] = input_object['model']
        # extra_info[g.MODEL_SELECTED] = ex_ai_dict[g.MODEL_SELECTED]
        criterion = input_object['criterion']
        is_classification = (criterion == 'classification')
        if is_classification :
             extra_info['pred_proba'] = True
        else:
             extra_info['pred_proba'] = False
        test_point_pred = test_data_processed.iloc[ind]
        # test_point_pred = test_point_pred["Predicted " + outcome].tolist()
        extra_info["g"] = g_orig
             
        raw_test_point = test_data_processed 
        try:
            response = get_explanation_bulk(
                                            train_data, outcome, criterion,
                                            test_point, test_point_pred,
                                            raw_test_point,
                                            extra_info)
            return response
        except ValueError as e:
            traceback.print_exc()
            return str(e)
        except Exception as e:
            traceback.print_exc()
            return 'Internal Server Error'
    except Exception as e:
        traceback.print_exc()
        return 'Internal Server Error'


def get_explanation_bulk(
               train_data, outcome, mode,
               test_point,
               test_point_pred,
               raw_test_point,
               extra_info):

    g = DotDict(extra_info["g"])
    tunable_params_dict = {}
    tunable_params_dict['training_data_propotion'] = g.MIN_R1_SAMPLED_TRAINING_DATA_PROPORTION
    np.random.seed(g.DEBUG_SEED_PERTURBATION)
    model_data = {}
    if g.SCALER in extra_info:
        model_data[g.SCALER] = extra_info[g.SCALER]
    else:
        # scaler = StandardScaler()
        # X = train_data.drop(outcome, axis=1)
        # scaler.fit_transform(X)
        model_data[g.SCALER] = None
        extra_info[g.SCALER] = None

    min_model_data = get_random_train_data(train_data, outcome, extra_info)
    model_data[g.RANDOM_TRAIN_DATA] = min_model_data
    extra_info['model_data'] = model_data
    if "N1_data" not in extra_info:
        if g.MULTINOMIAL_HISTOGRAM or g.EXAI_ENHANCE_PERFORMANCE or\
            (mode == "classification" and not g.LIME_FOR_CLASSIF) or\
            (mode == "regression" and not g.LIME_FOR_REGR):
            get_pdf_data(g, mode, train_data, outcome,
                         tunable_params_dict,
                         model_data,
                         extra_info
                        )

    return get_explanations_all_records(
                                        train_data, outcome,
                                        mode, test_point,
                                        test_point_pred,
                                        raw_test_point,
                                        extra_info)
