import numpy as np
import operator
import traceback
import pandas as pd
import pickle
from .exai_utils_explain import get_perturbed_points
from .exai_utils_explain import DotDict
from .exai_utils_explain import get_model_dictionary
from .exai_utils_explain import predict_results_from_service
from . import exai_explain as explain
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


FORK_ERROR_TIMEOUT = 1
FORK_EXPL_TIMEOUT = 20


def sample_points(csr, edges):
    '''
    For sampling some points from multinomial histogram.

    Args:
    csr: The dictionary having histogram bins as key and number of
         points to samples as value.
    edges: outer bin edges of each dimension of the training data.

    Returns:
    random_points: The array of sampled points.
    '''
    random_points = []
    for entry, value in csr:
        random_pt = []
        for bin_value, edge in zip(list(entry), edges):
            minimum = edge[bin_value - 1]
            maximum = edge[bin_value]
            random_pt.append(np.random.uniform(minimum, maximum, value))
            # for each feature we generate csr[entry] sample
        random_points.extend(np.array(random_pt).T)
    return random_points


def penalty_function(test_point, N1, g):
    # Normalizing samples before computing distance, distance computation on non-normalized features
    # will give abnormaly large values of distances.
    _test_point = test_point / np.linalg.norm(test_point)
    _N1 = N1 / np.linalg.norm(N1, axis=1, keepdims=True)
    euc_dist = ((_N1 - _test_point) ** 2).sum(axis=1)
    R_x = np.exp(-pd.Series(euc_dist))
    if g.USE_EUC_PENALTY: # Switch to toggle the use of penalty based on eucledian distance.
        penalty = np.sqrt(euc_dist)
    else: # Switch to toggle the use of penalty based on the exponent of eucledian distance.
        penalty = R_x.to_numpy()
    return np.multiply(N1, penalty[:, np.newaxis])


def _get_outer_edges(a, range):
    """
    This function is taken from Numpy library to determine the outer bin edges
    to use, from either the data or the range argument.

    Args:
    a: data for which we want the outer bin edges.
    range: range argument for which we want to verify the outer bin edges.

    Returns:
    first_edge: Left bin edge of the data.
    last_edge: Right bin edge of the data.
    """
    if range is not None:
        first_edge, last_edge = range
        if first_edge > last_edge:
            raise ValueError('max must be larger than min in range parameter.')
        if not (np.isfinite(first_edge) and np.isfinite(last_edge)):
            raise ValueError("supplied range of [{}, {}] is not finite".format(
                             first_edge, last_edge))
    elif a.size == 0:
        # handle empty arrays. Can't determine range, so use 0-1.
        first_edge, last_edge = 0, 1
    else:
        first_edge, last_edge = a.min(), a.max()
        if not (np.isfinite(first_edge) and np.isfinite(last_edge)):
            raise ValueError("autodetected range of [{}, {}] is not finite"
                             .format(first_edge, last_edge))

    # expand empty range to avoid divide by zero
    if first_edge == last_edge:
        first_edge = first_edge - 0.5
        last_edge = last_edge + 0.5

    return first_edge, last_edge


def numpy_histdd(D, bins, sample):
    '''
    Compute the multidimensional histogram of some data. This is taken from
    Numpy library.
    Args:
        D: Number of dimensions.
        bins: A tuple containing number of bins for each dimension.
        sample: The training data for which we want the multinomial histogram.
    Return:
        Ncount: A tuple with the bin number each sample falls into.
        edges: Bins edges of histogram.
    '''
    nbin = np.empty(D, int) 
    edges = D * [None]
    dedges = D * [None]
    try:
        M = len(bins)
        if M != D:
            raise ValueError('The dimension of bins must be equal\
                             to the dimension of the sample x.')
    except TypeError:
        # bins is an integer
        bins = D * [bins]

    range1 = (None,) * D
    # Create edge arrays
    for i in range(D):
        if np.ndim(bins[i]) == 0:
            if bins[i] < 1:
                raise ValueError('`bins[{}]` must be positive,\
                                 when an integer'.format(i))
            smin, smax = _get_outer_edges(sample[:, i], range1[i])
            try:
                n = operator.index(bins[i])

            except TypeError:
                raise TypeError("`bins[{}]` must be an integer,\
                                when a scalar".format(i))

            edges[i] = np.linspace(smin, smax, n + 1)
        else:
            raise ValueError('`bins[{}]` must be a scalar'.format(i))

        nbin[i] = len(edges[i])
        dedges[i] = np.diff(edges[i])
    # Compute the bin number each sample falls into.
    # avoid np.digitize to work around gh-11022
    Ncount = tuple(np.searchsorted(edges[i], sample[:, i],
                   side='right') for i in range(D))
    # Using digitize, values that fall on an edge are put in the right bin.
    # For the rightmost bin, we want values equal to the right edge to be
    # counted in the last bin, and not as an outlier.
    for i in range(D):
        # Find which points are on the rightmost edge.
        on_edge = (sample[:, i] == edges[i][-1])
        # Shift these points one bin to the left.
        Ncount[i][on_edge] -= 1
    return Ncount, edges


def multinomial_histogram(train_data, bins_index=0):
    '''
    Creating a multinomial histogram from the training data.
    The format of multinomial histogram is dictionary.
    Which keys are the tuples which contain bin numbers for each dimensional.
    And Values of the keys are the number of points which fall
    in that tuple of bin numbers.

    Args:
    train_data: The training data for which we want the multinomial histogram.

    Returns:
    csr_dict: Final multinomial histogram generated from the
              training data. The format of it is dictionary.
    edges: outer bin edges of each dimension of the training data.
    '''
    sample = train_data.to_numpy()
    N, D = sample.shape
    sample_T = sample.T
    bins = []
    for i in range(D):
        if len(np.unique(sample_T[i])) <= 2:
            bins.append(len(np.unique(sample_T[i])))
        else:
            bins.append(10)
    bins = tuple(bins)
    Ncount, edges = numpy_histdd(D, bins, sample)
    csr_dict = {}
    csr_ind = {}
    Ncount_t = np.array(Ncount).T
    bin_list = [10 * bins_index + bins_index for x in range(len(bins))]
    for index, i in enumerate(Ncount_t):
        if tuple(i + bin_list) in csr_dict.keys():
            csr_dict[tuple(i + bin_list)] += 1
            csr_ind[tuple(i + bin_list)] += [index]
        else:
            csr_dict[tuple(i + bin_list)] = 1
            csr_ind[tuple(i + bin_list)] = csr_ind.get(tuple(i + bin_list), [])
            csr_ind[tuple(i + bin_list)] += [index]     
    return csr_dict, edges, csr_ind


def sampling_from_multinomial_histogram(csr_dict, num_samples, edges):
    '''
    For sampling some random points from multinomial histogram.

    Args:
    csr_dict: Multinomial histogram or PDF of a training data.
              The format of it is dictionary.
    num_samples: Random nuumber of samples which we want to sample
                 from the Multinomial Histogram or PDF.
    edges: outer bin edges of each dimension of the training data.

    Returns:
    samples: The array which contain random points
             sampled from the training data.
    '''
    csr_items = sorted(csr_dict.items(), key=lambda kv: kv[1], reverse=True)
    total = sum(dict(csr_items).values())
    csr_items = [(k, v / float(total)) for k, v in csr_items]
    csr_temp = [(k, int(v * num_samples)) for k, v in csr_items]
    # How can we give this error to user instead of system crash?
    samples = []
    samples.extend(sample_points(csr_temp, edges))
    tot = num_samples - len(samples)
    while len(samples) < num_samples:
        csr_items = csr_items[:tot]
        if csr_temp[0][1] == 0.0:
            csr_temp = [(k, tot) for k, v in csr_items[:1]]
        else:
            csr_temp = [(k, int(v * tot)) for k, v in csr_items]
        samples.extend(sample_points(csr_temp, edges))
        tot = num_samples - len(samples)
    return samples


def get_N1_N2(g, mode, train_data, outcome, tunable_params_dict,
              model_data, debug, extra_info):
    '''
    To get the N1 and N2 samples with their outcome
    from the multinmial histogram.

    Args:
    train_data : Training data on which multinomial histogram will be
                 generated.
    outcome : Outcome variable of training data.

    Returns:
    N1_data : N1 samples sampled from multinomial histogram. It will be
             included in train data of explanation tree along with
             perturbed test points.
    N1_outcome : Black box prediction of N1_data.
    N2_data : N2 samples sampled from multinomial histogram. It will be
              test data of explanation tree.
    N2_outcome : Black box prediction of N2_data.
    '''
    orig_train_length = len(train_data)
    if orig_train_length > 10000:
        train_data = train_data.sample(n=int(max(
            g.TRAIN_SAMPLES_FOR_PDF, 10000))).reset_index(drop=True)
    count_series = train_data[outcome].value_counts()
    bins_index = 0
    data = train_data.drop(outcome, axis=1)
    hist = multinomial_histogram(data, bins_index)
    histogram, edges, csr_ind = hist
    if mode == "classification":
        final_histogram = histogram
        final_edges = edges
        final_csr_ind = csr_ind
        stop_flag = 0
        loop_count = 0
        while stop_flag == 0:
            tup_list = []
            for i in csr_ind:
                for label in count_series.index:
                    label_count = 0
                    for j in csr_ind[i]:
                        if train_data[outcome][j] == label:
                            label_count += 1
                    if label_count > g.LABEL_MIN_PERCENTAGE * count_series[label]:
                        tup_list.append(i)

            tup_list = list(set(tup_list))
            if len(tup_list) > 0:
                old_data = data
                for ind, tup in enumerate(tup_list):
                    if ind > 0:
                        data = old_data
                    del final_histogram[tup]
                    edges_list = []
                    bins_index += 1
                    data = data.iloc[final_csr_ind[tup]]
                    hist = multinomial_histogram(data, bins_index)
                    histogram, new_edges, csr_ind = hist
                    final_histogram.update(histogram)
                    del final_csr_ind[tup]
                    final_csr_ind.update(csr_ind)
                    for final_edge, new_edge in zip(final_edges, new_edges):
                        if len(new_edge) < 11:
                            for time in range(11 - len(new_edge)):
                                new_edge = np.append(new_edge, -np.inf)
                        if len(final_edge) < 11:
                            for time in range(11 - len(final_edge)):
                                final_edge = np.append(final_edge, -np.inf)
                        edges_list.append(np.append(final_edge, new_edge))
                    final_edges = edges_list
                loop_count += 1
                if loop_count == 4:
                    stop_flag = 1
            else:
                stop_flag = 1
        histogram, edges, csr_ind = final_histogram, final_edges, final_csr_ind
    
    N1_samples = int(max(g.N1_SAMPLES, 1000))
    N2_samples = int(max(g.N2_SAMPLES, 5000))
    N1_data = sampling_from_multinomial_histogram(
        histogram, N1_samples, edges)
    tr_cols = extra_info[g.RULE_LIME]['columns']
    if outcome in tr_cols:
        tr_cols.remove(outcome)
    N1_outcome = predict_results_from_service(
        pd.DataFrame(data=N1_data,
                     columns=tr_cols), outcome, model_data,
        extra_info)
    N2_data = sampling_from_multinomial_histogram(
        histogram, N2_samples, edges)
    N2_outcome = predict_results_from_service(
        pd.DataFrame(data=N2_data,
                     columns=tr_cols), outcome, model_data,
        extra_info)

    if mode == "classification":
        while len(np.unique(N1_outcome)) < train_data[outcome].nunique():
            N1_random_indices = np.random.choice(
                range(train_data.shape[0]),
                int(N1_samples),
                replace=True
            )
            N1_data = train_data.drop(outcome, axis=1).values[N1_random_indices]
            N1_outcome = train_data[outcome].values[N1_random_indices]
            N2_random_indices = np.random.choice(
                range(train_data.shape[0]),
                int(N2_samples),
                replace=True
            )
            N2_data = train_data.drop(outcome, axis=1).values[N2_random_indices]
            N2_outcome = train_data[outcome].values[N2_random_indices]

    if model_data[g.SCALER] is not None:
        scaler = get_model_dictionary(model_data[g.SCALER])
        N1_data = scaler.transform(N1_data)
        N2_data = scaler.transform(N2_data)
    if mode == 'classification':
        N1_outcome = N1_outcome.astype(np.string_)
        N2_outcome = N2_outcome.astype(np.string_)
    else:
        N1_outcome = N1_outcome.astype(np.float)
        N2_outcome = N2_outcome.astype(np.float)
    if debug:
        training_points = train_data.drop(outcome, axis=1)
        np.savetxt('train_data.csv', training_points, delimiter=",")
        np.savetxt('N1_points.csv', N1_data, delimiter=",")
        np.savetxt('N1_points_outcome.csv', N1_outcome,
                   delimiter=",", fmt='%s')
        np.savetxt('N2_points.csv', N2_data, delimiter=",")
        np.savetxt('N2_points_outcome.csv', N2_outcome,
                   delimiter=",", fmt='%s')
    return N1_data, N1_outcome, N2_data, N2_outcome


def get_all_perturbed_points(
    test_point, min_model_data, model_data,
    extra_info,
    tunable_params_dict, predict_results_from_service,
    mode, cov_of_train
    ):
    if "M1_points" in extra_info:
        return
    g = DotDict(extra_info["g"])
    Maximum_R1 = g.MAX_R1_SAMPLED_TRAINING_DATA_PROPORTION
    if g.MULTINOMIAL_HISTOGRAM:
        Maximum_R1 = g.MAX_R1_PDF_PROPORTION  
    tunable_params_dict_all = tunable_params_dict.copy()
    tunable_params_dict_all[
        'training_data_propotion'] = Maximum_R1 * g.PERTURBATION_SET_SIZE
    
    M1_points, M1_outcome = get_perturbed_points(
        test_point[0], min_model_data, model_data,
        extra_info,
        tunable_params_dict_all, predict_results_from_service,
        g.DEBUG, mode=mode, cov_of_train=cov_of_train)

    if g.ENHANCE_PERTURBED_POINTS:
        extra_info["M1_points"] = M1_points
        extra_info["M1_outcome"] = M1_outcome


def get_pdf_data(g, mode, train_data, outcome,
                  tunable_params_dict,
                  model_data,
                  extra_info
                ):
    tunable_params_dict['training_data_propotion'] = g.MIN_R1_PDF_PROPORTION
    max_score = -float('inf')
    Maximum_R1 = g.MAX_R1_PDF_PROPORTION
    N1_data, N1_outcome, N2_data, N2_outcome = get_N1_N2(
        g, mode, train_data, outcome, tunable_params_dict,
        model_data, g.DEBUG, extra_info)
    cov_of_train = np.cov(
        (train_data.drop(outcome, axis=1).to_numpy()).T)

    extra_info["N1_data"] = N1_data
    extra_info["N2_data"] = N2_data
    extra_info["N1_outcome"] = N1_outcome
    extra_info["N2_outcome"] = N2_outcome
    extra_info["cov_of_train"] = cov_of_train


def get_parallel_error(idx, chunks, args, retlist):
    dbglog(("inside get_parallel", idx, chunks))
    
    train_data, outcome, test_point, model_data, mode, extra_info,\
    predict_results_from_service, raw_test_point, bbox_test_pt_prediction,\
    N1_data, N2_data, N1_outcome, N2_outcome, cov_of_train, tunable_params_dict = args
    tunable_params_dict['training_data_propotion'] = chunks
    ret = find_min_error(train_data, outcome, test_point, model_data.copy(),
                   mode, extra_info,
                   predict_results_from_service, raw_test_point, bbox_test_pt_prediction,
                   N1_data, N2_data, N1_outcome, N2_outcome, cov_of_train,
                   tunable_params_dict.copy())
    retlist[idx] = ret


def get_random_train_data(train_data, outcome, extra_info):
    g = DotDict(extra_info["g"])
    a = g.TRAIN_DATA_PROPORTION
    N = g.MAX_THRESHOLD_FOR_TRAIN_SAMPLES
    # carve a random sample out of original training data
    num_of_train_samples = min(int(train_data.shape[0] * a), N)
    random_indices = np.random.choice(
        range(train_data.shape[0]),
        int(num_of_train_samples),
        replace=False
    )
    sampled_training_points = train_data.drop(outcome, axis=1).values[random_indices]
    sampled_training_points_outcome = train_data[outcome].values[random_indices]
    return [sampled_training_points, sampled_training_points_outcome]


def find_min_error(train_data, outcome, test_point, model_data, mode, extra_info,
                   predict_results_from_service, raw_test_point, bbox_test_pt_prediction,
                N1_data, N2_data, N1_outcome, N2_outcome, cov_of_train,
                tunable_params_dict):
    score = None
    dtree = None
    err = float('inf')
    dbg_errors = None
    np.random.seed(int(tunable_params_dict['training_data_propotion']*100))
    try:
        g = DotDict(extra_info["g"])
        # check error with this sample and scan for optimal parameters
        # with scan_optimal_params=True
        if g.MULTINOMIAL_HISTOGRAM:
            temp = explain.get_rule_explanations(
                test_point[0],
                model_data[g.RANDOM_TRAIN_DATA],
                mode, model_data, extra_info,
                predict_results_from_service,
                raw_test_point, tunable_params_dict, bbox_test_pt_prediction,
                scan_optimal_params=True, debug=g.DEBUG, N1_points=N1_data,
                N2_points=N2_data, N1_outcome=N1_outcome,
                N2_outcome=N2_outcome, cov_of_train=cov_of_train)
            err, score, m1_err, m1_wt, n1_err, n1_wt, feat, exp_str, dtree = temp 
            if g.DEBUG:
                dbg_errors = [m1_err, m1_wt, n1_err, n1_wt, feat, exp_str]
        else:
            temp = explain.get_rule_explanations(
                test_point[0], model_data[g.RANDOM_TRAIN_DATA], mode,
                model_data, extra_info, predict_results_from_service,
                raw_test_point, tunable_params_dict, bbox_test_pt_prediction,
                scan_optimal_params=True, debug=g.DEBUG)
            err = temp[0]
    except Exception as e:
        traceback.print_exc()
    return err, model_data[g.RANDOM_TRAIN_DATA], tunable_params_dict['training_data_propotion'], score, dtree, dbg_errors 


def get_parallel_explanations_pool(args):
    train_data, outcome, mode, test_point, raw_test_point, extra_info = args
    try:
        return get_exai_explanations(
            train_data, outcome, mode,
            test_point, raw_test_point,
            extra_info)
    except Exception as e:
        traceback.print_exc()


def get_parallel_explanations(rec_num, chunks, args, retlist):
    uid, did, mid, train_data, outcome, mode, test_point, test_point_pred, raw_test_point, extra_info = args
    g = DotDict(extra_info["g"])
    extra_info[g.TEST_PT_PRED] = test_point_pred[rec_num]
    raw_test_point_rec = raw_test_point.iloc[rec_num-1]
    ret = get_exai_explanations(uid, did, mid,
               train_data, outcome, mode,
               test_point[rec_num].reshape(1, -1),
               raw_test_point_rec,
               extra_info)
    retlist[rec_num] = ret
    

def get_exai_explanations(
               train_data, outcome, mode,
               test_point, raw_test_point,
               extra_info):
    """
        This state handles the request to display the interpretations made by LIME in module 3
        @param uid        user_id of the user
        @param did        dataset_id of the model
        @param mid        model_id of the model
        @param cmd        command entered by the user
        @param display    boolean prameter used to call the function first time 
    """
    g = DotDict(extra_info["g"])
    model_data = extra_info["model_data"]
    model_data['outcome'] = outcome
    confidence_score = None
    if (mode == "classification" and not g.LIME_FOR_CLASSIF) or\
        (mode == "regression" and not g.LIME_FOR_REGR):
        tunable_params_dict = {}
        param_value = 0.67
        # tunable_params_dict['training_data_propotion'] = 0.67
        tunable_params_dict['training_data_propotion'] =\
            g.MIN_R1_SAMPLED_TRAINING_DATA_PROPORTION
        Maximum_R1 = g.MAX_R1_SAMPLED_TRAINING_DATA_PROPORTION
        np.random.seed(g.DEBUG_SEED_PERTURBATION)
        min_err = float('inf')
        min_err_dtree = None
        conf_score = []
        prev_error = []
        r1_range = []
        d_tree_list = []
        if g.DEBUG:
            m1_error = []
            m1_error_points = []
            n1_error = []
            n1_error_points = []
            exp_string = []
            feat_imp = []

        min_model_data = model_data[g.RANDOM_TRAIN_DATA]
        if g.MULTINOMIAL_HISTOGRAM:
            tunable_params_dict['training_data_propotion'] =\
                g.MIN_R1_PDF_PROPORTION
            Maximum_R1 = g.MAX_R1_PDF_PROPORTION
            # get N1_data from extra_info
            N1_data = extra_info["N1_data"]
            N2_data = extra_info["N2_data"]
            N1_outcome = extra_info["N1_outcome"]
            N2_outcome = extra_info["N2_outcome"]
            cov_of_train = extra_info["cov_of_train"]
        if g.EXAI_ENHANCE_PERFORMANCE:
            N1_data = penalty_function(test_point[0], extra_info["N1_data"], g)
            N2_data = penalty_function(test_point[0], extra_info["N2_data"], g)
            N1_outcome = extra_info["N1_outcome"]
            N2_outcome = extra_info["N2_outcome"]
            cov_of_train = extra_info["cov_of_train"]
        bbox_test_pt_prediction = extra_info[g.TEST_PT_PRED]
        if not g.ONLY_PERTURBED_POINTS:
            get_all_perturbed_points(
                test_point, min_model_data, model_data,
                extra_info,
                tunable_params_dict, predict_results_from_service,
                mode, cov_of_train)
            chunks = [round(x,2) for x in np.arange(
                tunable_params_dict['training_data_propotion'],
                Maximum_R1 + g.PERTURBATION_TRAINING_DATA_INCREMENT_PROP,
                g.PERTURBATION_TRAINING_DATA_INCREMENT_PROP)
                     ]
            retval = []
            for chunk in chunks:
                tunable_params_dict['training_data_propotion'] = chunk
                ret = find_min_error(train_data, outcome, test_point, model_data.copy(),
                    mode, extra_info,
                    predict_results_from_service, raw_test_point, bbox_test_pt_prediction,
                    N1_data, N2_data, N1_outcome, N2_outcome, cov_of_train,
                    tunable_params_dict.copy())
                retval.append(ret)
            #args = (train_data, outcome, test_point, 
            #        model_data.copy(),
            #        mode, extra_info, predict_results_from_service,
            #        raw_test_point, bbox_test_pt_prediction,
            #        N1_data, N2_data, N1_outcome, N2_outcome, cov_of_train,
            #        tunable_params_dict)
            #retval = [None] * len(chunks)
            #fork_n_join_thread(chunks, get_parallel_error, args, retval, 100)
            for temp in retval:
                if temp is None:
                    continue
                t_err, t_model_data, t_param_value, t_score, t_dtree,\
                    t_dbg_err = temp
                prev_error.append(t_err)
                conf_score.append(t_score)
                r1_range.append(t_param_value)
                d_tree_list.append(t_dtree)
                if g.MULTINOMIAL_HISTOGRAM and g.DEBUG and\
                    t_dbg_err is not None:
                    m1_error.append(t_dbg_err[0])
                    m1_error_points.append(t_dbg_err[1])
                    n1_error.append(t_dbg_err[2])
                    n1_error_points.append(t_dbg_err[3])
                    exp_string.append(t_dbg_err[4])
                    feat_imp.append(t_dbg_err[5])
                if not g.MULTINOMIAL_HISTOGRAM:
                    if t_err < min_err:
                        min_err = t_err
                        min_model_data = t_model_data
                        param_value = t_param_value
                        min_err_dtree = t_dtree
                    # perfect explainer model achieved
                    if min_err == 0:
                        break
                    extra_info["min_err_dtree"] = min_err_dtree
        if g.MULTINOMIAL_HISTOGRAM:
            err_df = pd.DataFrame(prev_error, columns=['Prev_error'])
            error = [float(i)/max(prev_error) for i in prev_error]
            conf_score = [
                conf ** g.S2_N2_BETA_CONTEXT_AWARENESS for conf in conf_score]
            error = [err ** g.E1_N1M1_ALPHA_FIT_GOODNESS for err in error]
            composite_score = np.divide(conf_score, error)
            composite_score = [round(comp, 3) for comp in composite_score]
            r1_index = np.argmax(composite_score)
            param_value = r1_range[r1_index]
            tunable_params_dict['training_data_propotion'] = param_value
            min_err_dtree = d_tree_list[r1_index]
            extra_info["min_err_dtree"] = min_err_dtree
            if g.DEBUG:
                chart_df = pd.DataFrame(zip(r1_range, conf_score,
                                        m1_error_points, m1_error,
                                        n1_error_points, n1_error, prev_error,
                                        error, composite_score,
                                        feat_imp, exp_string),
                                        columns=["R1", "Confidence",
                                                 "M1_Points",
                                                 "M1_Error", "N1_Points",
                                                 "N1_Error", "Error",
                                                 "Sig(Error)",
                                                 "Composite",
                                              "Feature_Important_Dictionary",
                                              "Explanation"])
        else:
            # set the optimal parameters and rerun explanations
            model_data[g.RANDOM_TRAIN_DATA] = min_model_data
            extra_info["model_data"] = model_data
            tunable_params_dict['training_data_propotion'] = param_value
            if g.EXAI_ENHANCE_PERFORMANCE:
                tunable_params_dict['training_data_propotion'] = 1.0 
            if g.DEBUG:
                dbglog("Sample id %s : traininig data proportion %s for errr\
                    %s : seed %s : dataset %s : portion %s %s"%(0, param_value,
                    min_err, g.DEBUG_SEED_PERTURBATION, g.DEBUG_DATASET_NAME,
                    g.TRAIN_DATA_PROPORTION,
                    g.MAX_THRESHOLD_FOR_TRAIN_SAMPLES))

        if g.MULTINOMIAL_HISTOGRAM or g.EXAI_ENHANCE_PERFORMANCE:
            temp = explain.get_rule_explanations(
                test_point[0], model_data[g.RANDOM_TRAIN_DATA],
                mode, model_data, extra_info, predict_results_from_service,
                raw_test_point, tunable_params_dict,
                bbox_test_pt_prediction, scan_optimal_params=False,
                debug=g.DEBUG, N1_points=N1_data, N2_points=N2_data,
                N1_outcome=N1_outcome, N2_outcome=N2_outcome,
                cov_of_train=cov_of_train)
            feature_imp_dict, rule_lime_explanations, test_prediction,\
                confidence_score = temp[:4]
        else:
            temp = explain.get_rule_explanations(
                test_point[0], model_data[g.RANDOM_TRAIN_DATA],
                mode, model_data, extra_info, predict_results_from_service,
                raw_test_point, tunable_params_dict,
                bbox_test_pt_prediction, scan_optimal_params=False,
                debug=g.DEBUG)
            feature_imp_dict, rule_lime_explanations, test_prediction,\
                confidence_score = temp[:4]
    else:
        dbglog("Using Student teacher LIME Explanations")
        temp = get_lime_expls(
                    uid, did, mid, train_data,
                    outcome, test_point, model_data,
                    mode, extra_info,
                    predict_results_from_service,
                    raw_test_point)
        feature_imp_dict, rule_lime_explanations, test_prediction, confidence_score = temp
    return feature_imp_dict, rule_lime_explanations, test_prediction, confidence_score


def get_lime_expls(
    uid, did, mid, train_data,
    outcome, test_point, model_data,
    mode, extra_info,
    predict_results_from_service,
    raw_test_point
    ):
    g = DotDict(extra_info["g"])
    tr_cols = extra_info[g.RULE_LIME]['columns']
    if outcome in tr_cols:
        tr_cols.remove(outcome)
    sampled_training_points = train_data.drop(outcome, axis=1).values
    sampled_training_points_outcome = train_data[outcome].values
    train_data_all = [sampled_training_points, sampled_training_points_outcome]
    dbglog("Using LIME Explanations")
    lime_ans = get_lime_report(uid, did, mid, [test_point[0]],
                               model_data, 
                               predict_results_from_service, train_data_all[0],
                               tr_cols, None, 1000, mode, extra_info
                               )
    weight_list = []
    explanation_dict = dict()
    for lime_obj in lime_ans:
        feature_and_weights = lime_obj[0].as_list()
        features = list()
        weights = list()
        for feature, weight in feature_and_weights:
            split = feature.split("<")
            if len(split) == 1:
                split = feature.split(">")
            if len(split) == 2:
                feature_name = split[0].strip()
            else:
                feature_name = split[1].strip() 
            features.append(feature_name)
            if feature_name not in explanation_dict:
                explanation_dict[feature_name] = [(feature, abs(weight))]
            else:
                explanation_dict[feature_name].append((feature, abs(weight)))
            weights.append(abs(weight))
        weights = np.array(weights)
        weights = weights / sum(weights)
        weight_list.append(dict(zip(features, weights)))
    av_df = pd.DataFrame(weight_list).mean().round(2)
    md_df = pd.DataFrame(weight_list).median().round(2)
    sd_df = pd.DataFrame(weight_list).std().round(2)
    feature_imp_dict = dict(zip(av_df.index.tolist(), av_df.values))
    feature_imp_dict_all = dict(zip(av_df.index.tolist(), zip(av_df.values, sd_df.values, md_df.values)))
    #test_prediction = predict_results_from_service(uid, did, mid, pd.DataFrame(data=[test_point[0]], columns=extra_info[g.RULE_LIME]['columns']), extra_info=extra_info)[0]
    test_prediction = extra_info[g.TEST_PT_PRED]
    for feature_name in explanation_dict:
        explanations = explanation_dict[feature_name]
        explanations = sorted(explanations, key=lambda x: x[1], reverse=True)
        end_index = min(len(explanations), 5)
        explanation_dict[feature_name] = [explanations[x][0] for x in range(0, end_index)]

    if type(test_prediction) in [np.str_]:
        test_prediction = str(test_prediction)
    elif type(test_prediction) not in [str, np.string_, np.str_]:
        test_prediction = round(test_prediction, 2)
    rule_lime_explanations = explain.get_lime_explanations(uid, raw_test_point,
                                    extra_info[g.RULE_LIME]['columns'], 
                                    feature_imp_dict, extra_info[g.RULE_LIME]['ginfodict'],
                                    test_point[0], explanation_dict, extra_info) 
    dbglog(('Feature Importance Dictionary', feature_imp_dict, feature_imp_dict_all))
    for k in feature_imp_dict_all:
        dbglog((k, feature_imp_dict_all[k]))
    return feature_imp_dict, rule_lime_explanations, test_prediction, None


def get_explanations_pdf_api(uid,
                mode,
                outcome,
                N1,
                N2,
                M1,
                test_data,
                record_number,
                scaler,
                extra_info
            ):
    global g
    g = DotDict(extra_info["g"])
    new_cat_col_list = []
    record_number = int(record_number)
    test_data_without = test_data.drop(outcome, axis=1)
    orig_feat = test_data_without.columns
    features_selected = N1.drop(outcome, axis=1).columns.tolist()
    for test_col in test_data.columns:
        if test_col is not outcome:
            if test_data[test_col].dtype == object:
                new_cat_col_list.append(test_col)
            elif test_col not in features_selected:
                new_cat_col_list.append(test_col)
    test_data_outcome = test_data[[outcome]]
    test_data = create_dummy_train_features(test_data, new_cat_col_list)
    raw_test_point = test_data_without.iloc[[record_number-1]]
    out_type = N1[outcome].dtype
    if mode == 'regression':
        pred_proba = False
    else:
        pred_proba = True
    extra_info["pred_proba"] = pred_proba

    tr_cols = N1.columns.values.tolist()
    if outcome in tr_cols:
        tr_cols.remove(outcome)
    test_point = test_data.iloc[record_number - 1].reindex(tr_cols).values.reshape(
        1, -1).astype('float64')

    min_model_data = get_random_train_data(N1, outcome, extra_info)
    model_data = {}
    model_data[g.RANDOM_TRAIN_DATA] = min_model_data
    if scaler[0] is True:
        model_data[g.SCALER] = pickle.load(open(scaler[1], "rb"))
    else:
        model_data[g.SCALER] = None 
    extra_info['model_data'] = model_data
    bbox_test_pt_prediction = test_data_outcome[outcome][record_number-1]
    N1_data = N1.drop(outcome, axis=1).to_numpy()
    N2_data = N2.drop(outcome, axis=1).to_numpy()
    M1_data = M1.drop(outcome, axis=1).to_numpy()
    N1_outcome = N1[[outcome]].to_numpy()
    N2_outcome = N2[[outcome]].to_numpy()
    M1_outcome = M1[[outcome]].to_numpy()
    extra_info["N1_data"] = N1_data
    extra_info["N2_data"] = N2_data
    extra_info["N1_outcome"] = N1_outcome
    extra_info["N2_outcome"] = N2_outcome
    extra_info["M1_points"] = M1_data
    extra_info["M1_outcome"] = M1_outcome
    extra_info[g.TEST_PT_PRED] = bbox_test_pt_prediction
    extra_info["cov_of_train"] = None
    extra_info[g.RULE_LIME] = {'columns': features_selected}
    extra_info[g.STAT] = None
    extra_info[g.SCALER] = model_data[g.SCALER]
    extra_info['PDF_API'] = True
     
    feature_imp_dict, rule_lime_explanations, test_prediction, confidence_score = get_exai_explanations(uid, "1234_pdf_api", None,
                         None, outcome, mode,
                         test_point, raw_test_point,
                         extra_info
                        )
    rule_lime_explanations = str(rule_lime_explanations).replace(g.EXP_SEP, ',')
    response = {}
    response["explanation"] = rule_lime_explanations
    response["confidence"] = confidence_score.split(':')[-1]
    response["record_number"] = record_number
    response["prediction"] = bbox_test_pt_prediction
    response["feature_imp_dict"] = feature_imp_dict
    return response
 

def get_df_from_files(data_file_path, schema_path, outcome, is_clf=False):
    data_pointer = open(data_file_path, "r")
    schema_pointer = open(schema_path, "r")
    #data = list()
    #for every_line in data_pointer:
    #    data.append(every_line.replace("\n","").replace("\r","").split('\t'))
    cols = list()
    for every_line in schema_pointer:
        line = every_line.replace('\n', "").replace('\r', "")
        cols.append(line)
    df = pd.read_csv(data_file_path, names=cols, delimiter='\t')
    if outcome in df.columns:
        if is_clf:
            df[outcome] = df[outcome].astype('str')
        else:
            df[outcome] = pd.to_numeric(df[outcome], errors='ignore').round(4)
    return df
