import numpy as np
import pandas as pd
import pickle
from .exai_utils_explain import DotDict, handle_empty_params_dict,\
    get_perturbed_points, build_explanation_tree, get_feature_importance,\
    get_explanation_depth, get_decision_information, handle_missing_explainers,\
    modify_decision_information, get_explanation_string
from . import augi_data_insights as augi_di
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning) 
warnings.filterwarnings("ignore", category=FutureWarning)
g = None


def exponential_error(mode, scaler, points, points_outcome,
                      model_data, extra_info, dtree, scaled_test_sample,
                      debug=False):
    '''
    To compute and return error and weightage of sampled points using
    error_score function.

    Args:
    mode: classification/regression
    scaler: StandardScaler which is fitted on training data.
    points: Those points for which error and weightage required.
    rule_lime_dict: A dictionary having the following structure
                    {'ginfodict': ..., 'ccindx': ..., columns: ...}
                    where ginfodict stores the global information
                    dictionary
                    columns stores the column information
                    cat_col_indx stores those indices where columns[i]
                    is a categorical variable.
    scaled_test_sample: The scaled test point to get the local explanations
                        for a numpy array
    predict_fn: The function which makes the predictions

    Returns:
    error: Exponential weightage error between the prediction and outcome
           of points.
    R_x: Weightage given to non zero error on the basis of distance.
    '''
    rule_lime_dict = extra_info[g.RULE_LIME]
    model_predictions = points_outcome
    trees_predictions = dtree.predict(points)
    if mode == 'classification':
        model_predictions = [np.string_(st) for st in model_predictions]
    else:
        model_predictions = [np.float(st) for st in model_predictions]
    error, R_x = error_score(mode, model_predictions, trees_predictions,
                             scaled_test_sample[0], points, rule_lime_dict,
                             debug=debug)
    return error, R_x


#@timeit
def get_exp_metrics(mode, dtree, test_sample,
                    rule_lime_dict, tunable_params_dict, raw_test_point,
                    combined_near_points, combined_near_points_outcome,
                    extra_info,
                    scaler=None, predict_fn=None, debug=False):
    '''
    To get the explanation string and feature importance of test point
    on the basis of perturbed test points and sampled points from PDF
    of training data.

    Args:
    mode: classification/regression
    scaler: StandardScaler which is fitted on training data.
    combined_near_points: Combination of perturbed test points and
                          sampled points from PDF of training data.
    rule_lime_dict: A dictionary having the following structure
                    {'ginfodict': ..., 'ccindx': ..., columns: ...}
                    where ginfodict stores the global information
                    dictionary
                    columns stores the column information
                    cat_col_indx stores those indices where columns[i]
                    is a categorical variable.
    predict_fn: The function which makes the predictions

    Returns:
    exp_str: Determined explanation string of a test point.
    feature_imp_dict: Determined feature importance dictionary of test point
    node_list: The path of the leaf node at which test point lands up.
    '''
    if scaler is not None:
       scaled_test_sample = scaler.transform([test_sample])
    else:
        scaled_test_sample = test_sample.reshape(1, -1)
    # Get the feature importance dictionary
    feature_imp_dict = get_feature_importance(dtree, rule_lime_dict)
    feature_importance_before_pruning = dtree.feature_importances_
    # Counting the number of explanations before pruning
    num_explanations = get_explanation_depth(scaled_test_sample, dtree,
                                             rule_lime_dict)

    column_names = None
    global_info_dict = None
    if rule_lime_dict is not None:
        column_names = rule_lime_dict['columns']
        if 'ginfodict' in rule_lime_dict.keys():
            global_info_dict = rule_lime_dict['ginfodict']
    # Get the explanation and local feature importance
    path_dict, path_list, node_list = get_decision_information(scaled_test_sample, dtree,
                                                               column_names, global_info_dict,
                                                               scaler)
    if g.INCLUDE_MISSING_EXPLAINERS:
        path_dict, path_list = handle_missing_explainers(path_dict, path_list,
                                                         raw_test_point, scaled_test_sample,
                                                         combined_near_points, dtree,
                                                         column_names, global_info_dict,
                                                         scaler, feature_importance_before_pruning,
                                                         mode)
            
    modified_path_dict = modify_decision_information(path_list, path_dict, global_info_dict)
    exp_str = get_explanation_string(raw_test_point, path_list, modified_path_dict, extra_info,
                                     column_names, feature_imp_dict,
                                     global_info_dict, test_sample)
    return exp_str, feature_imp_dict, node_list


def acc_cov_calculation(mode, sample_points, sample_points_outcome, bbox_test_pt_prediction,
                        test_node_index, dtree, rule_lime_dict, rmse):
    '''
    For calculation of accuracy and coverage of leaf node where test
    point landed up.

    Args:
    mode: Classification or Regression
    sample_points: Sample points for which we want the coverage and
                   accuracy on test point node.
    sample_points_outcome: Outcome of sample points.
    test_node_index: Node in the Decision Tree where test point landed up.
    dtree: Built tree on training points (White Box Model).
    rule_lime_dict: A dictionary having the following structure
                    {'ginfodict': ..., 'ccindx': ..., columns: ...}
                    where ginfodict stores the global information dictionary
                    columns stores the column information
                    cat_col_indx stores those indices where columns[i]
                    is a categorical variable.
    rmse: RMSE for each node of built Decision Tree in
          regression mode (White Box Model).

    Returns:
    true_points_on_test_node: Number of sample points which landed up on
                              the same node where test point landed up and
                              their prediction is also same.
    points_on_test_node: Number of total sample points which landed up on
                         the same node where test point landed up.
    accuracy: accuracy of test point node on sample points.
    coverage: coverage of test point node on sample points.
    '''
    samples_node_index = list(dtree.apply(sample_points, check_input=True))
    samples_prediction = dtree.predict(
        pd.DataFrame(data=sample_points, columns=rule_lime_dict['columns']))
    points_on_test_node = 0
    true_points_on_test_node = 0
    mse_n2 = 0
    for ind, node_ind in zip(
            range(len(samples_prediction)),
            samples_node_index):
        if test_node_index[0] == node_ind:
            points_on_test_node += 1
            if mode == 'classification':
                if type(sample_points_outcome[ind]) == 'numpy.bytes_':
                    if sample_points_outcome[ind].decode() == samples_prediction[ind]:
                        true_points_on_test_node += 1
                else:
                    if sample_points_outcome[ind] == samples_prediction[ind]:
                        true_points_on_test_node += 1
            else:
                mse_n2 += (round(float(sample_points_outcome[ind])) - round(
                    bbox_test_pt_prediction))**2
    try:
        mse_n2 = mse_n2 / float(points_on_test_node)
    except ZeroDivisionError:
        mse_n2 = mse_n2
    coverage = points_on_test_node / float(len(sample_points))
    if points_on_test_node == 0:
        dbglog(("No sample points landed up on the same" +\
            "node where test point is landed up"))
        return 0, 0, 0, 0
    else:
        if mode == 'classification':
            accuracy = true_points_on_test_node / float(points_on_test_node)
            return true_points_on_test_node, points_on_test_node, coverage, accuracy
        else:
            rmse_n2 = np.sqrt(mse_n2)
            accuracy = abs(bbox_test_pt_prediction) / (abs(
                bbox_test_pt_prediction) + pow(rmse_n2, g.RMSE_POWER_N))
            return  rmse_n2, points_on_test_node, coverage, accuracy


def error_score(mode, mp, tp, tst, cd, rd, debug_suffix=None,
                eps=1e-8, debug=False):
    # compute L_x = (M(x) - T(x))^2
    try:
        tpdf = pd.DataFrame(tp, columns=['outcome'])
        mpdf = pd.DataFrame(mp, columns=['outcome'])
        if mode == 'classification':
            tpd = pd.get_dummies(tpdf['outcome'])
            mpd = pd.get_dummies(mpdf['outcome'])
            tpd_cols_list = tpd.columns.values.tolist()
            mpd_cols_list = mpd.columns.values.tolist()
            tpd_union_mpd_cols = list(set(tpd_cols_list) | set(mpd_cols_list))
            for col in list(set(tpd_union_mpd_cols) - set(tpd_cols_list)):
                tpd[col] = 0
            for col in list(set(tpd_union_mpd_cols) - set(mpd_cols_list)):
                mpd[col] = 0
            L_x = ((mpd - tpd)**2).sum(axis=1)
        else:
            L_x = ((mpdf['outcome'] - tpdf['outcome'])**2)
            #L_x = pd.Series(L_x['outcome'].values)
        
        # Normalizing samples before computing distance, distance computation on non-normalized features
        # will give abnormaly large values of distances.
        _tst = tst/np.linalg.norm(tst)
        _cd = cd/np.linalg.norm(cd, axis=1, keepdims=True)

        # compute R_x = e^[(x-x')**2]
        # tstdf = pd.DataFrame([_tst], columns=rd['columns'])
        # cdf = pd.DataFrame(_cd, columns=rd['columns'])
        
        # Commenting this line to split it into two parts
        #R_x = np.exp(((cdf - pd.concat([tstdf]*len(cdf), ignore_index=True))**2).sum(axis=1))
        # euc_dist = ((cdf - pd.concat([tstdf]*len(cdf), ignore_index=True))**2).sum(axis=1)
        euc_dist = ((_cd - _tst) ** 2).sum(axis=1)
        R_x = np.exp(-pd.Series(euc_dist))
        penalty = 1
        if g.USE_EUC_PENALTY: # Switch to toggle the use of penalty based on eucledian distance.
            penalty = np.sqrt(euc_dist).sum()
        elif g.USE_EXP_PENALTY: # Switch to toggle the use of penalty based on the exponent of eucledian distance.
            penalty = R_x.sum()

        if debug_suffix:
            pickle.dump((tpdf, mpdf, tpd, mpd, L_x, _tst, _cd, R_x), open('debug.' + str(debug_suffix) + '.pkl', 'w'))

        # Cost computation, divide by penalty to scale the case
        # based on data distribution, added eps to avoid division by 0
        cost = np.dot(L_x, R_x) / (penalty + eps)
        if debug:
            indexes = [i for i, x in enumerate(L_x.to_list()) if x != 0]
            temp_list = R_x.to_list()
            # consider only non zero values
            result_filtered = [temp_list[i] for i in indexes]
            return cost, result_filtered
        return cost, [None]
    except Exception as e:
        traceback.print_exc()
        dbglog(("Exception while calculating error score", e))
        return float('inf'), [float('inf')]


#@timeit
def get_explanations_with_multinomial_histograms(
        mode, model_data, test_sample, scaler, rule_lime_dict,
        combined_near_points, combined_near_points_outcome, predict_fn,
        dtree, raw_test_point, tunable_params_dict, scan_optimal_params,
        debug, N1_points, N1_outcome, N2_points, N2_outcome, M1_points, M1_outcome,
        tot_count, sig_th_tuple, p_hat, dtree_inflate, rmse,
        bbox_test_pt_prediction, wbox_test_pt_prediction, extra_info):
    '''
    Get English like explanations when g.MULTINOMIAL_HISTOGRAM is TRUE.
    '''
    if scaler is not None:
        scaled_test_sample = scaler.transform([test_sample])
    else:
        scaled_test_sample = test_sample.reshape(1, -1)
    # Get index of dtree node whete test sample has landed
    # and compute accuracy and coverage of that node for N2 points
    test_node_index = list(dtree.apply(scaled_test_sample,
            check_input=True))
    acc, count_node, coverage, accuracy = acc_cov_calculation(
                    mode, N2_points, N2_outcome, bbox_test_pt_prediction,
                    test_node_index, dtree, rule_lime_dict, rmse)
    accuracy = np.array([accuracy])
    coverage = np.array([coverage])
    
    # Apply sigmoid on accuracy and coverage and get penalized score
    if g.AUGI_SIGMOID_SCORING:
        conf_score, sig_th_tuple, s_coverage, s_accuracy =\
                        augi_di.scoring_model_sigmoid("LE", accuracy, coverage, sig_th_tuple)
        conf_score_before = conf_score[0]
    else:
        inflated_coverage = dtree_inflate.predict(coverage.reshape(-1,1))
        conf_score_before = np.vectorize(lambda i: min(i, 0.98))(
                                         inflated_coverage[0] * accuracy[0])
    p_hat = p_hat[test_node_index][0]
    conf_score, b, penalty = augi_di.penalizing_scores(
                    p_hat, tot_count, conf_score_before, "LE")[:-1]
    conf_score = augi_di.apply_user_perception(conf_score)    
    conf_score, penalty = conf_score[0], penalty[0]

    # Scan for optimal parameters
    if scan_optimal_params:
        # Return lowest confidence score and highest prediction error
        # when white_box and black_box predictions are different
        if mode == "classification" and bbox_test_pt_prediction != wbox_test_pt_prediction:
                return 1, -float('inf'), None, None, None, None,\
                    None, None
        error, L_x = exponential_error(
           mode, scaler, combined_near_points,
           combined_near_points_outcome, model_data, extra_info, dtree,
           scaled_test_sample, debug)

        return error, conf_score, None, None, None, None, None, None
    return None, conf_score, None, None, None, None, None, None


#@timeit
def get_rule_explanations(
        test_sample, random_train_data, mode, model_data,
        extra_info, predict_fn=None,
        raw_test_point=None, tunable_params_dict=None,
        bbox_test_pt_prediction=None,
        scan_optimal_params=False, debug=False, N1_points=None, N2_points=None,
        N1_outcome=None, N2_outcome=None, cov_of_train=None):
    '''
    Get English like explanations as well
    as local feature importance

    Args:
        test_sample: The test point to get the local explanations
                     for, a numpy array
        random_train_data: A list containing the sampled training data and the outcome
        mode: classification/regression
        predict_fn:  The function which makes the predictions
        scaler:  StandardScaler which is fitted on training data.
        rule_lime_dict: A dictionary having the following structure
                        {'ginfodict': ..., 'ccindx': ..., columns: ...}
                        where ginfodict stores the global information
                        dictionary
                        columns stores the column information
                        cat_col_indx stores those indices where columns[i]
                        is a categorical variable.
        stat_df: dataframe containing the statistics of numerical columns
        raw_test_point: Will be used to display the actual categorical value. other labels might not be available in processed data.
        tunable_params_dict: If you need to override default parameters
                        tunable_params_dict['training_data_propotion'] : the percentage of training data present in the overall collection of points
                        tunable_params_dict['method_of_perturb']: 'normal_binomial' and 'manual_bias'
                        tunable_params_dict['decision_tree_params'] : dict having the hyperparameters of decision tree built
                        tunable_params_dict['perturb_method_params']: dict having categorical_change_chance, numerical_perturb_range if normal binomial
                                                                      else threshold if manual_bias
                        tunable_params_dict['pruning_alpha']: the value of alpha where the pruning should stop.
    Returns:
        Dictionary with columns, local feature importance pairs
        English like explanations which tries to explain the prediction
        The prediction made by the model
    '''
    global g
    g = DotDict(extra_info["g"])
    scaler = model_data[g.SCALER]
    rule_lime_dict = extra_info[g.RULE_LIME]
    stat_df = None # extra_info[g.STAT]

    assert len(test_sample.shape) == 1, 'Only one test data can be explained at a time'
    tunable_params_dict = handle_empty_params_dict(tunable_params_dict)

    # Generate the datapoints
    if g.MULTINOMIAL_HISTOGRAM:
        M1_points, M1_outcome = get_perturbed_points(
            test_sample, random_train_data, model_data,
            extra_info,
            tunable_params_dict, predict_fn,
            debug, mode=mode, cov_of_train=cov_of_train)
            
        combined_near_points = np.r_[N1_points, M1_points]
        combined_near_points_outcome = np.r_[N1_outcome, M1_outcome]
    elif g.EXAI_ENHANCE_PERFORMANCE:
        combined_near_points = np.r_[N1_points]
        combined_near_points_outcome = np.r_[N1_outcome]
    else:
        combined_near_points, combined_near_points_outcome = get_perturbed_points(
            test_sample, random_train_data, model_data,
            extra_info,
            tunable_params_dict, predict_fn,
            debug, mode=mode, cov_of_train=cov_of_train)
    

    combined_near_points_outcome_df = pd.DataFrame(
        combined_near_points_outcome, columns=['outcome'])
    avg_std_dev_outcome = np.mean(np.std(
        pd.get_dummies(combined_near_points_outcome_df['outcome'])))
    if debug:
        dbglog(("Mean of stddev of combined points",
            avg_std_dev_outcome))
        # if scan_optimal_params and g.AVG_STD_DEV_OUTCOME < 0.28:
        #    # TODO make this a configurable threshold [:DONE]
        #    # there must be enough variability in training labels
        #    # for explainer model
        #     return float('inf')

    # Build the model
    # TODO verify the need of weighted tree in regression enviorenment
    weights = None
    if mode == "classification": # and type(combined_near_points_outcome[0]) == 'np.bytes_':
        combined_near_points_outcome_new = []
        for i in combined_near_points_outcome:
            try:
                i = i.decode()
                combined_near_points_outcome_new.append(i)
            except:
                combined_near_points_outcome_new.append(i)
        combined_near_points_outcome = np.array(combined_near_points_outcome_new)
    dtree = build_explanation_tree(
        mode, combined_near_points, combined_near_points_outcome,
        extra_info, tunable_params_dict, weights, rule_lime_dict['columns'] , debug,
        scaler)
    if mode == 'classification':
        di_scores = augi_di.get_classification_score(dtree, local_g=g)
        scores, maj_class, all_maj_count, tot_count, confidence,\
            coverage, sig_th_tuple, p_hat, dtree_inflate = di_scores[:-5]
        rmse = None
    else:
        di_scores = augi_di.get_regression_score(dtree, local_g=g)
        scores, rmse, tot_count, confidence, coverage,\
            sig_th_tuple, p_hat, dtree_inflate = di_scores[:-5]

    if predict_fn is not None:
        if scaler is not None:
            scaler = pickle.load(open(scaler, "rb"))
            scaled_test_sample = scaler.transform([test_sample])
        else:
            scaled_test_sample = test_sample.reshape(1, -1)
        wbox_test_pt_prediction = dtree.predict(scaled_test_sample)[0]

        if g.MULTINOMIAL_HISTOGRAM or g.EXAI_ENHANCE_PERFORMANCE:
            if mode == 'classification':
                if not g.EXAI_ENHANCE_PERFORMANCE:
                    M1_outcome = M1_outcome.astype(np.string_)
                else:
                    M1_outcome = None
                    M1_points = None
                bbox_test_pt_prediction = np.string_(bbox_test_pt_prediction)
                wbox_test_pt_prediction = np.string_(wbox_test_pt_prediction)
            else:
                if not g.EXAI_ENHANCE_PERFORMANCE:
                    M1_outcome = M1_outcome.astype(np.float)
                else:
                    M1_outcome = None
                    M1_points = None
                bbox_test_pt_prediction = np.float(bbox_test_pt_prediction)
                wbox_test_pt_prediction = np.float(wbox_test_pt_prediction)
            if not scan_optimal_params and debug:
                dbglog(("bbox, wbox", bbox_test_pt_prediction, wbox_test_pt_prediction))
            # TODO: should we check for error on non-pruned tree or on
            # pruned tree (as is done later
            
            error, conf_score, m1_error, m1_L_x, n1_error, n1_L_x,\
                feature_imp_dict, exp_str =\
                    get_explanations_with_multinomial_histograms(
                        mode, model_data, test_sample, scaler,
                        rule_lime_dict, combined_near_points,
                        combined_near_points_outcome, predict_fn, dtree,
                        raw_test_point, tunable_params_dict, scan_optimal_params,
                        debug, N1_points, N1_outcome, N2_points, N2_outcome, M1_points,
                        M1_outcome, tot_count, sig_th_tuple, p_hat, dtree_inflate, rmse,
                        bbox_test_pt_prediction, wbox_test_pt_prediction, extra_info)

            if scan_optimal_params:
                return error, conf_score, m1_error, m1_L_x, n1_error, n1_L_x,\
                   feature_imp_dict, exp_str, dtree
        else:
            if scan_optimal_params:
                if scaler:
                    data = scaler.inverse_transform(combined_near_points)
                else:
                    data = combined_near_points
                model_predictions = bbox_test_pt_prediction
                trees_predictions = dtree.predict(combined_near_points)
                if mode == 'classification':
                    model_predictions = np.string_(model_predictions)
                    trees_predictions = np.string_(trees_predictions)
                if debug:
                    pickle.dump(
                        (model_predictions, trees_predictions), open(
                            'predictions.pkl', 'w'))
                error, R_x = error_score(
                    mode, model_predictions, trees_predictions,
                    scaled_test_sample[0],
                    combined_near_points, rule_lime_dict)
                return error, None, None, None, None, None, None, None
    exp_str, feature_imp_dict, node_list = get_exp_metrics(
        mode, dtree, test_sample, rule_lime_dict,
        tunable_params_dict, raw_test_point, combined_near_points,
        combined_near_points_outcome, extra_info, scaler, predict_fn, debug)
    # The score should be max of scores in the node_list, i.e. maximum
    # of scores of any nodes along the path to the leaf. Also we should
    # never show a score of 1.0 (100%), dilute 100% down to 99%. 1 2 50 55 100
    exp_str_confidence = None
    if g.MULTINOMIAL_HISTOGRAM or g.EXAI_ENHANCE_PERFORMANCE:
        conf_score = max(0.25, conf_score)
        exp_str_confidence = str(int(round(conf_score, 2) * 100)) + "%" 
    else:
        exp_str_confidence = str(int(min(0.99, max([
            round(scores[t], 2) for t in node_list])) * 100)) + "%"
    if predict_fn is not None:
        if type(bbox_test_pt_prediction) in [np.unicode_]:
            bbox_test_pt_prediction = str(bbox_test_pt_prediction)
        elif type(bbox_test_pt_prediction) not in [str, np.string_]:
            bbox_test_pt_prediction = np.round(bbox_test_pt_prediction, 2)
    else:
        bbox_test_pt_prediction = None
    return feature_imp_dict, exp_str[len(g.EXP_SEP) + 1:],\
        bbox_test_pt_prediction, exp_str_confidence, None, None, None, None, dtree


#@timeit
def get_lime_explanations(uid, raw_test_point, column_names, feature_imp_dict, global_info_dict, test_sample, explanation_dict, extra_info):
    '''
        Given the LIME explanation dictionary, 
        returns the explanation in human understandable manner
    '''
    g = DotDict(extra_info["g"])
    imp_cols = sorted(feature_imp_dict, key=feature_imp_dict.get, reverse=True)
    path_dict = dict()
    path_list = []
    # We generate path list and path dictionary. Path dictionary has indicies as keys and {operator, threshold, type} as it's values.
    for index, path_feature in enumerate(imp_cols):
        var_expl = explanation_dict[path_feature][0]
        splits = var_expl.split(path_feature)
        if '' in splits:
            splits.remove('')
        if len(splits) == 1:
            if '<' in splits[0]:
                if '<=' in splits[0]:
                    threshold = float(splits[0][splits[0].index('<=') + 3:])
                else:
                    threshold = float(splits[0][splits[0].index('<') + 2:])
                operator = '<='
            else:
                if '>=' in splits[0]:
                    threshold = float(splits[0][splits[0].index('>=') + 3:])
                else:
                    threshold = float(splits[0][splits[0].index('>') + 2:])
                operator = '>'
            dict_len = len(path_dict)
            path_dict[dict_len] = dict()
            path_dict[dict_len][path_feature] = {'operator': operator, 'threshold': threshold, 'type': global_info_dict[path_feature]['type']}
            path_list.append(path_feature)
        else:
            lower_bound, upper_bound = splits
            if '<' in lower_bound:
                lower_threshold = float(lower_bound[:lower_bound.index('<') - 1])
                lower_operator = '>'
                dict_len = len(path_dict)
                path_dict[dict_len] = dict()
                path_dict[dict_len][path_feature] = {'operator': lower_operator, 'threshold': lower_threshold, 'type': global_info_dict[path_feature]['type']}
                path_list.append(path_feature)
            if '<' in upper_bound:
                if '<=' in upper_bound:
                    upper_threshold = float(upper_bound[upper_bound.index('<=') + 3:])
                else:
                    upper_threshold = float(upper_bound[upper_bound.index('<') + 2:])
                upper_operator = '<='
                dict_len = len(path_dict)
                path_dict[dict_len] = dict()
                path_dict[dict_len][path_feature] = {'operator': upper_operator, 'threshold': upper_threshold, 'type': global_info_dict[path_feature]['type']}
                path_list.append(path_feature)
    modified_path_dict = modify_decision_information(path_list, path_dict, global_info_dict)
    exp_str = get_explanation_string(uid, raw_test_point, path_list, modified_path_dict, extra_info, column_names, feature_imp_dict,
                                          global_info_dict, test_sample)
    return exp_str[len(g.EXP_SEP)+1:]
    
