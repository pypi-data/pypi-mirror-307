import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from copy import deepcopy
from .augi_dtree_utils import prune, print_tree, get_distribution, is_leaf
from collections import defaultdict

g = None


class DotDict(object):
    def __init__(self, user_dict):
        for key in user_dict:
            setattr(self, key, user_dict[key])
    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError
        return self.get(attr, None)


def get_model_dictionary(model_path):
    model_obj = pickle.load(open(model_path, "rb"))
    return model_obj


def distribution_aware_local_sampling(val, distribution, num_samples=10, std_dev=0.13, act_std=None, alpha=0.65):
    '''
        Generates the value around the val considering the distribution
        given by the user
    '''
    if act_std is None:
        act_std = np.std(distribution)
    bins = np.histogram_bin_edges(distribution, bins='auto')
    bin_midpoints = bins[:-1] + np.diff(bins)/2
    pdf_x = np.histogram(distribution, bins = bins, density=True)[0]
    normal_data = np.random.normal(val, scale=(act_std*std_dev), size=2000)
    normal_data = np.clip(normal_data, np.min(distribution), np.max(distribution))
    pdf_y = np.histogram(normal_data, bins = bins, density=True)[0]
    c = (1-alpha)*pdf_x + alpha*pdf_y
    c = c/c.sum()
    cdf = np.cumsum(c)
    cdf = cdf / cdf[-1]
    values = np.random.rand(num_samples)
    value_bins = np.searchsorted(cdf, values)
    random_from_cdf = bin_midpoints[value_bins]
    return random_from_cdf


def generate_samples_around_test_split(test_sample, num_samples, threshold, scaler=None):
    '''
    Generate points near the test_sample
    Around the numerical columns, generate within the 15 percent
    of standard deviation of that column
    Around categorical columns, flip the one hot encoding
    15 percent of the time

    Args:
    test_sample: the test point around which the points are to be generated
    num_samples: The number of new points to generate around
    threshold: The random chance above which the samples would be modified.
    scaler: the scaler fitted on the training data. training data statistics will be derived using this.
                               the test sample
    Returns:
    The generated near points
'''
    dbglog('Manual Bias Sampling selected.')
    if scaler is not None:
        test_sample = scaler.transform(test_sample.reshape(1, -1))[0]
    new_sample = np.copy(test_sample)
    new_samples = np.zeros((num_samples, test_sample.shape[0]), dtype=np.float64)
    for j in range(num_samples):
        for i in range(test_sample.shape[0]):
            random_number = np.random.random_sample([1])
            # perturbation for both numeric and categorical variables
            if random_number < threshold:
                new_sample[i] = test_sample[i] + (0.1 * random_number)[0]
                if (new_sample[i] >= 1.0):
                    new_sample[i] = test_sample[i] - (0.1 * random_number)[0]
            else:
                new_sample[i] = test_sample[i] + (0.5 * random_number)[0]
                if (new_sample[i] >= 1.0):
                    new_sample[i] = test_sample[i] - (0.5 * random_number)[0]
        new_samples[j] = new_sample
    return new_samples


def generate_samples_around_test(mode, test_sample, num_samples, scaler_path=None,
                                 numerical_perturb_range=0.13, 
                                 std_dev=None, sampled_training_data=None, cov_of_train=None):
    '''
    Generate points near the test_sample
    Around the numerical columns, generate within the 15 percent
    of standard deviation of that column
    Around categorical columns, flip the one hot encoding
    15 percent of the time

    Args:
    test_sample: the test point around which the points are to be generated
    std_dev: the training data whose statistics will be used to generate
                the new points
    cat_col_indx: The indices which correspond to categorial columns
    num_samples: The number of new points to generate around
                               the test sample
    categorical_change_chance: The chance of the categorical variable getting it's category changed
    numerical_perturb_range: the propotion of perturbation to be done w.r.t. to the standard deviation of a numerical column
    :param std_dev: if scaler is None, the standard deviation expected across each column should be provided in this parameter
    Returns:
    The generated near points
'''
    if g.ONLY_PERTURBED_POINTS:
        numerical_perturb_range = g.PERTURBATION_STDDEV_RANGE
        num_samples = g.PERTURBATION_NUM_SAMPLES
    if g.DISTRIBUTION_AWARE_SAMPLING:
        numerical_perturb_range = 0.13
        num_samples = g.PERTURBATION_NUM_SAMPLES
    if scaler_path is not None:
        scaler = get_model_dictionary(scaler_path)
        std_dev = scaler.scale_
    if std_dev is None:
        return None
    near_generated_points = np.zeros(
        (num_samples, test_sample.shape[0]),
        dtype=np.float64
    )
    np.random.seed(42)
    if g.MULTINOMIAL_HISTOGRAM:
        numerical_perturb_range = g.PERTURBATION_COVARIANCE_RANGE
        # If train data has only 1 column. It can happen in text data where
        # user used only sentiment text derived predictor.
        if cov_of_train.shape == ():
            near_generated_points = np.random.normal(
                test_sample, cov_of_train * numerical_perturb_range,
                size=num_samples)
            near_generated_points = np.append(
                near_generated_points, test_sample).reshape(-1, 1)
        else:
            numerical_perturb_range_list = numerical_perturb_range *\
                np.identity(len(cov_of_train))
            near_generated_points = np.random.multivariate_normal(
                test_sample, cov_of_train * numerical_perturb_range_list,
                size=num_samples)
            near_generated_points = np.r_[near_generated_points, [test_sample]]
    else:
        for i in range(test_sample.shape[0]):
            # Do a normal sampling
            std_i = std_dev[i]
            if g.DISTRIBUTION_AWARE_SAMPLING:
                dbglog((numerical_perturb_range, num_samples, g.PROP_OF_LOCAL_DATA, 'HYPER PARAMS OF LOCAL SAMPLING'))
                near_generated_points[:, i] = distribution_aware_local_sampling(test_sample[i], sampled_training_data[:,i], std_dev=numerical_perturb_range, num_samples=num_samples, act_std = std_i, alpha=g.PROP_OF_LOCAL_DATA)
            else:
                near_generated_points[:, i] = np.random.normal(
                    test_sample[i], scale=(numerical_perturb_range * std_i) / 1.0,
                    size=num_samples)
        near_generated_points = np.r_[near_generated_points, [test_sample]]
    if scaler is not None:
        near_generated_points = scaler.transform(near_generated_points)
    return near_generated_points


def handle_empty_params_dict(tunable_params_dict):
    """
        Populates the hyper parameter dictionary with default options
        if user didn't supply the params for that key
    :param tunable_params_dict: Hyper parameters supplied by the user
    :return: Hyper parameters with the default recommended parameters
    """
    if tunable_params_dict is None:
        tunable_params_dict = {}
    if 'training_data_propotion' not in tunable_params_dict:
        tunable_params_dict['training_data_propotion'] = 0.2
    if 'method_of_perturb' not in tunable_params_dict:
        tunable_params_dict['method_of_perturb'] = 'normal_binomial'
    if 'perturb_method_params' not in tunable_params_dict:
        tunable_params_dict['perturb_method_params'] = {'categorical_change_chance': 0.15,
                                                        'numerical_perturb_range': 0.13}
    if 'decision_tree_params' not in tunable_params_dict:
        tunable_params_dict['decision_tree_params'] = {'max_depth': 16, 'random_state': 42}
    if 'pruning_alpha' not in tunable_params_dict:
        tunable_params_dict['pruning_alpha'] = float('inf')
    if 'min_number_of_explanation_after_prune' not in tunable_params_dict:
        tunable_params_dict['min_number_of_explanation_after_prune'] = 3
    return tunable_params_dict


from sklearn.tree._tree import TREE_LEAF
def prune_index(inner_tree, index):
     # turn node into a leaf by "unlinking" its children
     inner_tree.children_left[index] = TREE_LEAF
     inner_tree.children_right[index] = TREE_LEAF


def build_explanation_tree(mode, X, y, extra_info, tunable_params_dict=None, weights=None,
                           columns=None, debug=False, scaler=None):
    """
    Builds decision tree which then will be used for generating the explanation
    :param mode: Mode should be either classification or regression
    :param X: The perturbed test data on which explanation tree will be constructed
    :param y: The predictions made by the model on the perturbed test data
    :param tunable_params_dict: Hyper parameters supplied by the user
    :return:
    """
    global g
    g = DotDict(extra_info["g"])
    if "min_err_dtree" in extra_info and extra_info["min_err_dtree"] is not None:
        return extra_info["min_err_dtree"]
    tunable_params_dict = handle_empty_params_dict(tunable_params_dict)
    # Build the model
    if mode == 'classification':
        tunable_params_dict['decision_tree_params']['criterion'] = 'entropy'
        if g.MULTINOMIAL_HISTOGRAM and g.LE_CLASS_BALANCE:
            tunable_params_dict['decision_tree_params']['class_weight'] = 'balanced'
        dtree = DecisionTreeClassifier(**tunable_params_dict['decision_tree_params'])
    else:
        tunable_params_dict['decision_tree_params']['criterion'] = 'mse'
        if g.MULTINOMIAL_HISTOGRAM:
            tunable_params_dict['decision_tree_params']['min_samples_leaf'] = 5 
        dtree = DecisionTreeRegressor(**tunable_params_dict['decision_tree_params'])
    dtree.fit(X, y, sample_weight=weights)
    tree_copy = deepcopy(dtree)
    if g.ENABLE_LE_PRUNING:
        distribution, nodes_leaves = get_distribution(tree_copy, X, y)
        print_tree(tree_copy, columns, scaler, distribution,
               graph_file='original_dtree.dot' if debug else None)
        pruned_nodes = prune(tree_copy, X, y, mode, distribution, nodes_leaves,
                             debug=debug, local_g=g)
        for node in pruned_nodes:
            prune_index(tree_copy.tree_, node)
        print_tree(tree_copy, columns, scaler, distribution,
               graph_file='pruned_dtree.dot' if debug else None)
    return tree_copy


def get_feature_importance(dtree, rule_lime_dict=None):
    """

    :param dtree: The fitted decision tree built by the user
    :param rule_lime_dict: A dictionary having the following structure
                        {'ginfodict': ..., 'ccindx': ..., columns: ...}
                        where ginfodict stores the global information
                        dictionary
                        columns stores the column information
                        cat_col_indx stores those indices where columns[i]
                        is a categorical variable.
                        If this is empty, the column names will be numeric.
    :return: The feature importance dictionary
    """
    # Calculate the feature importance dictionary beforehand
    importances = dtree.feature_importances_
    importances_indices = np.argsort(-importances)[:5]
    if rule_lime_dict is None:
        rule_lime_dict = dict()
        rule_lime_dict['columns'] = list(range(1, dtree.tree_.n_features + 1))
    features_and_importances = np.c_[rule_lime_dict['columns'], importances].tolist()
    top_features_and_importances = [features_and_importances[x] for x in importances_indices]
    feature_imp_dict = {t[0]: round(float(t[1]), 4) for t in top_features_and_importances}
    return feature_imp_dict


def get_explanation_depth(test_point, dtree, rule_lime_dict=None):
    """
    Gets the explanation depth on the user given point
    :param test_point:
    :param dtree:
    :param rule_lime_dict:
    :return: The number of explanations needed to explain the prediction for the given test point
    """
    if len(test_point.shape) == 1:
        test_point = test_point.reshape(1, -1)
    dpath = dtree.decision_path(test_point).indices
    dpath = dpath[:-1]  # The last node is a leaf node
    num_explanations = 0
    seen_cols = []
    #if 'ginfodict' not in rule_lime_dict.keys():
    rule_lime_dict = None
    for node in dpath:
        if rule_lime_dict is None:
            column_name = dtree.tree_.feature[node]
        else:
            column_name = rule_lime_dict['columns'][dtree.tree_.feature[node]]
            if 'text_col_name' in rule_lime_dict['ginfodict'][column_name]:
                if g.GLOVE_COLS in column_name:
                    continue
                column_name = rule_lime_dict['ginfodict'][column_name]['text_col_name']
            elif 'category' in rule_lime_dict['ginfodict'][column_name]:
                column_name = rule_lime_dict['ginfodict'][column_name]['col_name']
            else:
                pass
        if column_name in seen_cols:
            continue
        else:
            num_explanations += 1
            seen_cols.append(column_name)
    return num_explanations


def get_decision_information(test_sample, dtree, column_names=None, global_info_dict=None, scaler=None):
    """
    Get the path list and path dictionary for the test sample, given the fitted decision tree
    :param test_sample: the test sample provided by user
    :param dtree: the fitted decision tree
    :param column_names: the column names which should be used
    :param global_info_dict: more documentation can be found in explain.py get_rule_explanation function about this
    :param scaler: more documentation can be found in explain.py get_rule_explanation function about this
    :return: path_list, path_dict
    """
    # Get the decision path
    node_index = dtree.decision_path(test_sample).indices
    if scaler is None:
        mul_factor = np.ones(dtree.tree_.n_features)
        add_factor = np.zeros(dtree.tree_.n_features)
    else:
        mul_factor = scaler.scale_
        add_factor = scaler.mean_
    if column_names is None:
        column_names = list(range(1, dtree.tree_.n_features + 1))  # Numerical assignment of columns
    path_dict = {}
    path_list = []
    for index, node in enumerate(node_index):
        # We check if we are not in the leaf
        if is_leaf(dtree.tree_, node):
            continue
        col_idx = dtree.tree_.feature[node]
        column_name = column_names[col_idx]
        global_info_dict = None
        if global_info_dict is None:
            column_type = 'numerical'
        else:
            column_type = global_info_dict[column_name]['type']
        threshold = dtree.tree_.threshold[node]
        unscaled_threshold = threshold * \
                             mul_factor[col_idx] + add_factor[col_idx]
        unscaled_threshold = np.round(unscaled_threshold, 2)
        if index != len(node_index) - 1:
            # Do we go under or over the threshold ?
            if (dtree.tree_.children_left[node] == node_index[index + 1]):
                threshold_sign = "<="
            else:
                threshold_sign = ">"
            path_dict[index] = dict()
            path_dict[index][column_name] = {
                'operator': threshold_sign,
                'threshold': unscaled_threshold,
                'type': column_type}
            path_list.append(column_name)
    return path_dict, path_list, node_index


def get_all_tree_paths(dtree, combined_near_points):

    train_data_decision_paths = dtree.decision_path(combined_near_points)

    all_paths = dict()
    leaves = set()
    leaf_to_sample_index = defaultdict(list)
    for i in range(combined_near_points.shape[0]):
        curr_path = train_data_decision_paths[i].indices
        curr_leaf = curr_path[-1]
        leaf_to_sample_index[curr_leaf].append(i)
        if curr_leaf not in leaves: 
            all_paths[curr_leaf] = curr_path
            leaves.add(curr_leaf)

    return all_paths, leaf_to_sample_index


def handle_missing_explainers(path_dict, path_list, raw_test_sample, test_sample, combined_near_points, dtree, column_names=None, global_info_dict=None, scaler=None, feature_importance_before_pruning=None, mode='classification'):

    '''
        Function to include any missing important features in explanation.
        path_dict: dictionary which stores theexplanation from the decision path of test sample.
        path_list: list to store the part of decision path, included in explanation.
        raw_test_sampled: Unprocessed test sample to check for the consistancy of explanation.
        test_sample: preprocessed test sample.
        combined_near_points: sampled+perturbed data for training of explainer tree.
        dtree: trained explainer tree
        column_name: features names.
        global_info_dict: dictonary containing information regarding original features.
        scaler: Feature normalizer
        feature_importance_before_pruning: Feature importance from the unpruned tree.
    '''

    # Test sample is scaled
    # Combined near point is also scaled

    if scaler is None:
        mul_factor = np.ones(dtree.tree_.n_features)
        add_factor = np.zeros(dtree.tree_.n_features)
    else:
        mul_factor = scaler.scale_
        add_factor = scaler.mean_
    if column_names is None:
        column_names = list(range(1, dtree.tree_.n_features + 1))  # Numerical assignment of columns

    column_name_to_index_map = {b:a for a,b in enumerate(column_names)}

    decision_path = dtree.decision_path(test_sample).indices
    decision_leaf = decision_path[-1]

    # EXtracting all paths from decision tree
    all_paths, leaf_to_sample_index = get_all_tree_paths(dtree, combined_near_points)
    path_to_feature = {k:dtree.tree_.feature[all_paths[k][:-1]] for k in all_paths.keys()} # Last value is leaf hence, there is no feature

    # Extracting all features within margin
    feature_importances = dtree.feature_importances_
    if feature_importance_before_pruning is not None:
        feature_importances = feature_importance_before_pruning

    if g.PICK_TOP_FEATURES is None:
        most_important_feature = feature_importances.max()
        importance_to_include =  most_important_feature * (1 - g.LOCAL_FEATURE_IMPORTANCE_MARGIN)
        features_to_include = np.where(np.array(feature_importances) >= importance_to_include)[0]
    else:

        feature_indexes = np.argsort(feature_importances)[::-1][:g.PICK_TOP_FEATURES]
        important_features = feature_importances[feature_indexes]
        important_features = important_features / np.sum(important_features)

        most_important_feature = important_features.max()
        max_importance_to_include = most_important_feature * (1 - g.MAX_LOCAL_FEATURE_IMPORTANCE_MARGIN) # Not being used in this block
        #features_to_include = feature_indexes[np.where(important_features >= importance_to_include)[0]]
        importance_to_include = [important_features[0]]
        features_to_include = [feature_indexes[0]]
        for i in range(1, len(feature_indexes)):
            if (importance_to_include[-1]*(1-g.LOCAL_FEATURE_IMPORTANCE_MARGIN) <= important_features[i]) and (max_importance_to_include <= important_features[i]):
                importance_to_include.append(important_features[i])
                features_to_include.append(feature_indexes[i])
            else: break
        #features_to_include = get_important_features_based_on_global_name_ARCHIVED(feature_importances, column_names, global_info_dict)

    # Removing those features which are present in the original decision path
    features_to_include = np.setdiff1d(features_to_include, path_to_feature[decision_leaf])

    if len(features_to_include) == 0: # If all the important features are present in the original decision path, then nothing to do further.
        return path_dict, path_list

    # Extracting label information for every leaf
    if mode == 'classification':
        leaf_label = {i:np.argmax(dtree.tree_.value[i][0]) for i in leaf_to_sample_index.keys()}
    if mode == 'regression':
        pred_reg_value = np.squeeze(dtree.tree_.value)
        leaf_label = {i:pred_reg_value[i] for i in leaf_to_sample_index.keys()}

    # Filtering required paths based on leaf and importance information
    test_label = leaf_label[decision_leaf]

    if mode == 'classification':
        condition = lambda x: leaf_label[x] == test_label
    if mode == 'regression':
        std = np.std(list(leaf_label.values()))
        upper = test_label + std
        lower = test_label - std
        condition = lambda x: leaf_label[x] >= lower and leaf_label[x] <= upper

    required_leaf = []
    for k in leaf_label.keys():
        if k != decision_leaf and condition(k):
            if np.intersect1d(features_to_include, path_to_feature[k]).shape[0] > 0:
                required_leaf.append(k)

    if len(required_leaf) == 0:
        return path_dict, path_list

    # Computing euclidean distance information
    decision_leaf_avg_sample = np.mean(combined_near_points[leaf_to_sample_index[decision_leaf]], axis=0)

    leaf_dist = {}
    min_dist = float('inf')
    min_dist_k = None
    for k in required_leaf:
        m = np.mean(combined_near_points[leaf_to_sample_index[k]], axis=0)
        leaf_dist[k] = np.sqrt(np.sum((m - decision_leaf_avg_sample)**2))
        #leaf_dist[k] = np.sum(np.abs(m - decision_leaf_avg_sample))
        if leaf_dist[k] < min_dist:
            min_dist = leaf_dist[k]
            min_dist_k = k


    # Changes to handle fix in explanation text
    requried_leaf_after_euc_filetering = []
    sorted_distances = sorted(leaf_dist.items(), key=lambda x:x[1])

    not_included_features = features_to_include.copy()
    total_paths_scan = 0
    for s in sorted_distances:
        total_paths_scan += 1
        node_index = all_paths[s[0]]
        local_path_dict, local_path_list = get_local_paths(dtree, node_index, not_included_features, column_names, mul_factor, add_factor, global_info_dict=global_info_dict)

        consistent_local_path_dict, consistent_local_path_list = get_consistent_local_path_dict(raw_test_sample, local_path_list, local_path_dict, global_info_dict=global_info_dict)
        consistent_column_ids = [column_name_to_index_map[col] for col in consistent_local_path_list]
        not_included_features = np.setdiff1d(not_included_features, consistent_column_ids)

        for index, feat in enumerate(consistent_local_path_list):
            path_dict[len(path_list)] = consistent_local_path_dict[index]
            path_list.append(feat)

        if len(not_included_features) == 0: break


    return path_dict, path_list


def get_local_paths(dtree, node_index, not_included_features, column_names, mul_factor, add_factor, global_info_dict=None):
    
    local_path_dict = dict()
    local_path_list = []

    for index, node in enumerate(node_index):

        col_idx = dtree.tree_.feature[node]
        if is_leaf(dtree.tree_, node) or col_idx not in not_included_features:
            continue
        column_name = column_names[col_idx]
        if global_info_dict is None:
            column_type = 'numerical'
        else:
            column_type = global_info_dict[column_name]['type']
        threshold = np.round(dtree.tree_.threshold[node], 2)
        unscaled_threshold = threshold * \
                             mul_factor[col_idx] + add_factor[col_idx]
        unscaled_threshold = np.round(unscaled_threshold, 2)
        if index != len(node_index) - 1:
            # Do we go under or over the threshold ?
            if (dtree.tree_.children_left[node] == node_index[index + 1]):
                threshold_sign = "<="
            else:
                threshold_sign = ">"

        local_path_dict[len(local_path_list)] = dict()
        local_path_dict[len(local_path_list)][column_name] = {
            'operator': threshold_sign, 'threshold': unscaled_threshold, 'type': column_type}
        local_path_list.append(column_name)

    return local_path_dict, local_path_list


def get_consistent_local_path_dict(raw_test_sample, local_path_list, local_path_dict, global_info_dict=None):
    
    modified_local_path_dict = modify_decision_information(local_path_list, local_path_dict, global_info_dict=global_info_dict)
 
    consistent_dict = dict()
    for k in modified_local_path_dict.keys():
        try:
            val = raw_test_sample[k]
        except KeyError as e:
            continue
        
        feature_info_dict = modified_local_path_dict[k]
        if feature_info_dict['operator'] == '>':
            if 'type' in feature_info_dict and feature_info_dict['type'] == 'numerical':
                if float(val) > feature_info_dict['threshold']:
                    consistent_dict[k] = feature_info_dict
                    
        elif feature_info_dict['operator'] == '>=':
            if 'type' in feature_info_dict and feature_info_dict['type'] == 'numerical':
                if float(val) >= feature_info_dict['threshold']:
                    consistent_dict[k] = feature_info_dict
                    
        elif feature_info_dict['operator'] == '<':
            if 'type' in feature_info_dict and feature_info_dict['type'] == 'numerical':
                if float(val) < feature_info_dict['threshold']:
                    consistent_dict[k] = feature_info_dict
                    
        elif feature_info_dict['operator'] == '<=':
            if 'type' in feature_info_dict and feature_info_dict['type'] == 'numerical':
                if float(val) <= feature_info_dict['threshold']:
                    consistent_dict[k] = feature_info_dict
                    
        elif feature_info_dict['operator'] == 'in range':
            v1, v2 = feature_info_dict['threshold'].split(', ')
            if float(v1) > float(v2): v1, v2 = v2, v1
            if float(val) >= float(v1) and float(val) <= float(v2):
                consistent_dict[k] = feature_info_dict
                
        elif feature_info_dict['operator'] == '==':
            if str(val) == str(feature_info_dict['threshold']):
                consistent_dict[k] = feature_info_dict
                
        elif feature_info_dict['operator'] == '!=':
            if str(val) != str(feature_info_dict['threshold']):
                consistent_dict[k] = feature_info_dict
    
    keep_local_path_list = []
    keep_local_path_dict = dict()
    if len(consistent_dict) > 0:
        for index, feat in enumerate(local_path_list):
            ld = list(local_path_dict[index].keys())[0] 
            if global_info_dict is not None:
                if global_info_dict[ld]['col_name'] in consistent_dict.keys():
                    keep_local_path_dict[len(keep_local_path_list)] = local_path_dict[index]
                    keep_local_path_list.append(feat)
            else:
                return keep_local_path_dict, keep_local_path_list
    return keep_local_path_dict, keep_local_path_list


def modify_decision_information(path_list, path_dict, global_info_dict=None):
    modified_path_dict = {}
    if global_info_dict is None:
        global_info_dict = dict()
    for index, col_name in enumerate(path_list):
        if col_name not in global_info_dict:
            global_info_dict[col_name] = dict()
            global_info_dict[col_name]['type'] = 'numerical'
        if global_info_dict[col_name]['type'] == 'categorical':
            actual_col_name = global_info_dict[col_name]['col_name']
            if path_dict[index][col_name]['operator'] == '>':
                modified_operator = '=='
            else:
                # override '!=' if the condition happens to be 'feature <= 1.0'
                if path_dict[index][col_name]['threshold'] == 1.0:
                    modified_operator = '=='
                else:
                    modified_operator = '!='
            modified_threshold = global_info_dict[col_name]['category']
            if actual_col_name in modified_path_dict:
                if modified_path_dict[actual_col_name]['operator'] == '!' and path_dict[index][actual_col_name][
                    'operator'] == '!':
                    modified_path_dict[actual_col_name]['threshold'] += ', ' + \
                                                                        path_dict[index][actual_col_name]['threshold']
            else:
                modified_path_dict[actual_col_name] = {
                    'operator': modified_operator, 'threshold': modified_threshold}
        else:
            if col_name in modified_path_dict:
                if modified_path_dict[col_name]['operator'] != 'in range':
                    previous_op = modified_path_dict[col_name]['operator']
                    current_op = path_dict[index][col_name]['operator']
                    previous_threshold = modified_path_dict[col_name]['threshold']
                    current_threshold = path_dict[index][col_name]['threshold']

                    if previous_op == '>' and current_op == '<=' and current_threshold > previous_threshold:
                        modified_path_dict[col_name]['operator'] = 'in range'
                        modified_path_dict[col_name]['threshold'] = '{}, {}'.format(
                            previous_threshold, current_threshold)
                    elif previous_op == '<=' and current_op == '>' and previous_threshold > current_threshold:
                        modified_path_dict[col_name]['operator'] = 'in range'
                        modified_path_dict[col_name]['threshold'] = '{}, {}'.format(
                            current_threshold, previous_threshold)
                    elif previous_op == '>' and current_op == '>' and current_threshold > previous_threshold:
                        modified_path_dict[col_name]['threshold'] = current_threshold
                    elif previous_op == '<=' and current_op == '<=' and current_threshold < previous_threshold:
                        modified_path_dict[col_name]['threshold'] = current_threshold
                    else:
                        continue
                else:
                    min_thresh, max_thresh = modified_path_dict[col_name]['threshold'].split(
                        ',')
                    min_thresh = float(min_thresh)
                    max_thresh = float(max_thresh)
                    current_threshold = path_dict[index][col_name]['threshold']
                    min_thresh = min(current_threshold, min_thresh)
                    max_thresh = max(current_threshold, max_thresh)
                    modified_path_dict[col_name]['threshold'] = '{}, {}'.format(
                        min_thresh, max_thresh)
            else:
                modified_path_dict[col_name] = path_dict[index][col_name]
    return modified_path_dict


def get_perturbed_points(
        test_sample, random_train_data, model_data,
        extra_info,
        tunable_params_dict=None, predict_fn=None, debug=False,
        mode='classification', cov_of_train=None):
    """

    :param test_sample: The test sample around which the points will be generated
    :param random_train_data: The random training sample which will be used to get the perturbed points
    :param rule_lime_dict: A dictionary having the following structure
                        {'ginfodict': ..., 'ccindx': ..., columns: ...}
                        where ginfodict stores the global information
                        dictionary
                        columns stores the column information
                        cat_col_indx stores those indices where columns[i]
                        is a categorical variable.
                        If this is empty, it will assume all the columns are numeric.
    :param scaler: StandardScaler which is fitted on training data. If this is none, no preprocessing is assumed
    :param stat_df: dataframe containing the statistics of numerical columns. If empty, it will be calculated on the fly.
    :param tunable_params_dict: If you need to override default parameters
                        tunable_params_dict['training_data_propotion'] : the percentage of training data present in the overall collection of points
                        tunable_params_dict['method_of_perturb']: 'normal_binomial' and 'manual_bias'
                        tunable_params_dict['decision_tree_params'] : dict having the hyperparameters of decision tree built
                        tunable_params_dict['perturb_method_params']: dict having categorical_change_chance, numerical_perturb_range if normal binomial
                                                                      else threshold if manual_bias
                        if empty, default values will be used
    :param predict_fn: The function which makes the predictions. If not supplied, the predictions won't be generated
    :param debug: If you want to debug the function. Should be set to False in production.
    :return:
    """
    global g
    g = DotDict(extra_info["g"])
    tunable_params_dict = handle_empty_params_dict(tunable_params_dict)
    if "M1_points" in extra_info and (g.ENHANCE_PERTURBED_POINTS or 'PDF_API' in extra_info):
        #np.random.seed(g.DEBUG_SEED_PERTURBATION)
        Maximum_R1 = g.MAX_R1_SAMPLED_TRAINING_DATA_PROPORTION
        if g.MULTINOMIAL_HISTOGRAM:
            Maximum_R1 = g.MAX_R1_PDF_PROPORTION
        m1_prop = tunable_params_dict['training_data_propotion']
        M1_all_points = extra_info["M1_points"]
        M1_all_outcome = extra_info["M1_outcome"]
        len_M1 = M1_all_points.shape[0]
        M1_samples = int(
                (m1_prop / Maximum_R1) *
                (len_M1 / g.PERTURBATION_SET_SIZE - 1)) + 1
        m1_random_indices = np.random.choice(
            range(len_M1),
            M1_samples,
            replace=True
        )
        M1_points = M1_all_points[m1_random_indices]
        M1_outcome = M1_all_outcome[m1_random_indices]
        return M1_points, M1_outcome
 
    scaler_path = model_data[g.SCALER]
    rule_lime_dict = extra_info[g.RULE_LIME]
    stat_df = None # extra_info[g.STAT]
    rule_lime_dict['ginfodict'] = dict()
    rule_lime_dict['ccindx'] = []
    if rule_lime_dict is None:
        rule_lime_dict = dict()
        rule_lime_dict['columns'] = list(range(test_sample.shape[0]))
    if (isinstance(random_train_data, tuple) or isinstance(random_train_data, list)) and len(random_train_data) == 2:
        sampled_training_points, sampled_training_points_outcome = random_train_data
    else:
        sampled_training_points = random_train_data
    if g.MULTINOMIAL_HISTOGRAM:
        num_samples = int(
            g.N1_SAMPLES * tunable_params_dict['training_data_propotion'])
    else:
        num_samples = int(sampled_training_points.shape[0] * (
            1.0 / tunable_params_dict['training_data_propotion'] - 1))
    if tunable_params_dict['method_of_perturb'] == 'normal_binomial':
        categorical_change_chance = tunable_params_dict['perturb_method_params']['categorical_change_chance']
        numerical_perturb_range = tunable_params_dict['perturb_method_params']['numerical_perturb_range']
        if scaler_path is None:
            # Step 1: Ensure everything is numeric
            for col in sampled_training_points.columns:
                sampled_training_points[col] = pd.to_numeric(sampled_training_points[col], errors='coerce')
            std_dev = np.std(sampled_training_points, axis=0)
            std_dev = std_dev.values
        else:
            std_dev = None
        near_generated_points = generate_samples_around_test(
            mode, test_sample, num_samples, scaler_path, numerical_perturb_range,
            std_dev, sampled_training_points, cov_of_train=cov_of_train)
    else:
        threshold = tunable_params_dict['perturb_method_params']['threshold']
        near_generated_points = generate_samples_around_test_split(test_sample, num_samples, threshold, scaler)
    # We need to clip out the generated points into max and min
    if scaler_path is not None:
        scaler = get_model_dictionary(scaler_path)
        unscaled_near_generated_points = scaler.inverse_transform(near_generated_points)
    else:
        unscaled_near_generated_points = near_generated_points
    for i in range(test_sample.shape[0]):
        if i in rule_lime_dict['ccindx']:
            unscaled_near_generated_points[:, i] = np.clip(unscaled_near_generated_points[:, i], 0, 1)
            # or alternatively just use the absolute values
            # unscaled_near_generated_points[:,i] = np.absolute(unscaled_near_generated_points[:,i])
            pass
        else:
            # Clip the generated points to lie between max and min value if the column is numerical column
            if stat_df is not None:
                selected_stat_df = stat_df[stat_df['Variable Name'] == rule_lime_dict['columns'][i]]
                if not selected_stat_df.empty:
                    min_val, max_val = \
                        stat_df[stat_df['Variable Name'] == rule_lime_dict['columns'][i]][
                            ['Min value', 'Max Value']].values[0]
                    unscaled_near_generated_points[:, i] = np.clip(unscaled_near_generated_points[:, i], min_val,
                                                      max_val)
    if scaler_path is not None:
        near_generated_points = scaler.transform(unscaled_near_generated_points)
    else:
        near_generated_points = unscaled_near_generated_points

    if predict_fn is not None:
        near_generated_points_prediction = predict_fn(pd.DataFrame(
            data=unscaled_near_generated_points, columns=rule_lime_dict[
            'columns']), model_data['outcome'], model_data, extra_info)
    if scaler_path is not None:
        scaled_sampled_train_points = scaler.transform(sampled_training_points)
    else:
        scaled_sampled_train_points = sampled_training_points.values
    if debug:
        np.savetxt('test_sample.csv', test_sample, delimiter=",")
        if stat_df is not None:
            stat_df.to_csv('stat_df.csv')
        if scaler is not None:
            np.savetxt('scaled_sampled_train_points.csv', scaled_sampled_train_points, delimiter=",")
        np.savetxt('sampled_training_points.csv', sampled_training_points, delimiter=",")
        np.savetxt('near_generated_points.csv', near_generated_points, delimiter=",")
        np.savetxt('unscaled_near_generated_points.csv', unscaled_near_generated_points, delimiter=",")
    combined_near_points_outcome = None
    
    if not g.ONLY_PERTURBED_POINTS and not g.MULTINOMIAL_HISTOGRAM:
        combined_near_points = np.r_[
            scaled_sampled_train_points, near_generated_points]
        if predict_fn is not None:
            combined_near_points_outcome = np.r_[
                sampled_training_points_outcome, near_generated_points_prediction]
            if mode == 'classification':
                combined_near_points_outcome = combined_near_points_outcome.astype(
                    np.string_)
            else:
                combined_near_points_outcome = combined_near_points_outcome.astype(
                    np.float)
    else:
        combined_near_points = near_generated_points
        if predict_fn is not None:
            combined_near_points_outcome = near_generated_points_prediction
    if debug:
        np.savetxt('combined_near_points.csv', combined_near_points, delimiter=",")
        np.savetxt('sampled_training_points_outcome.csv', sampled_training_points_outcome, delimiter=",", fmt='%s')
        if predict_fn is not None:
            np.savetxt('near_generated_points_prediction.csv', near_generated_points_prediction, delimiter=",", fmt='%s')
            np.savetxt('combined_near_points_outcome.csv', combined_near_points_outcome, delimiter=",", fmt='%s')
    return combined_near_points, combined_near_points_outcome


def find_if_text_column(col, text_columns):
    text_column = None
    is_text_column = False
    if g.TOPICS_COLS in col:
        is_text_column = True
        text_column = col.split(g.TOPICS_COLS)[0]
    if g.CONCEPT_COLS in col:
        is_text_column = True
        text_column = col.split(g.CONCEPT_COLS)[0]
    for text_col in text_columns:
        if text_col in col:
            is_text_column = True
            text_column = text_col
        if is_text_column:
            break
    return is_text_column, text_column


def get_explanation_string(raw_test_point,
                           path_list,
                           modified_path_dict,
                           extra_info,
                           column_names=None,
                           feature_imp_dict=None,
                           global_info_dict=None,
                           test_sample=None,
                           from_pdf=False):
    global g
    g = DotDict(extra_info["g"])
    exp_str = ""
    seen_cols = {}
    if column_names is None:
        column_names = list(range(1, raw_test_point.shape[1]+1))
    if feature_imp_dict is None:
        feature_imp_dict = dict()
        for col in column_names:
            feature_imp_dict[col] = 1./len(column_names)
    if global_info_dict is None:
        global_info_dict = dict()
        for col in column_names:
            global_info_dict[col] = dict()
            global_info_dict[col]['type'] = 'numerical'
    if test_sample is None:
        test_sample = [float(x) for x in raw_test_point.values[0]]
    text_columns = [global_info_dict[col]['col_name'] for col in global_info_dict if
                    global_info_dict[col]['type'] == 'text']
    seen_text_columns = []
    for col in path_list:
        feature = col
        if global_info_dict[col]['type'] == 'categorical':
            feature = global_info_dict[col]['col_name']  # col is one hot encoded, we change it to category
        if feature in seen_cols:
            continue
        else:
            seen_cols[feature] = 1

        current_col_idx = column_names.index(col)
        if col in global_info_dict and global_info_dict[col]['type'] == 'numerical':
            actual_val = round(test_sample[current_col_idx], 2)
            thresh = str(modified_path_dict[col]['threshold'])
            operator = modified_path_dict[col]['operator']
            if operator == '>' and actual_val == thresh:
                operator = '>='
        elif col in global_info_dict and global_info_dict[col]['type'] == 'categorical':
            actual_val = global_info_dict[col]['category']
            thresh = str(modified_path_dict[feature]['threshold'])
            operator = modified_path_dict[feature]['operator']
        """
        example:
        The 'employee_evaluation' was predicted as 'good' because:
            fruit is kiwi and not equal to any of {orange, guava, apple} 
            deal_in_Million is 70M and that happens to be in range {60, 90}

            if <col> is categorical and operator is "==":
                    '<col>' is '<actual value>' 
            else:
                    '<col>' is '<actual value>' and '<operator in words>' '<value in words>'

            <operator in words>:
                "!=": " not equal to any of "
                "<=": " that happens to be less than or equal to "
                ">": " that happens to be more than " 
                "in range": " that happens to be in range "

            <value in words>:
                numeric, categorical
                numeric, numeric
                {categorical, categorical}
        """
        is_text_column = False
        if not g.DEBUG_ENABLED:
            is_text_column, text_column = find_if_text_column(col, text_columns)
        if is_text_column:
            if text_column in seen_text_columns:
                continue
            else:
                seen_text_columns.append(text_column)
                type_of_text = col[col.rfind(
                    '_derived_'):]  # User's column can have _derived_ as well. so we find the last occurence.
                if g.GLOVE_COLS in type_of_text:
                    del seen_text_columns[-1]
                    continue
                if type_of_text == g.DECORUM:
                    actual_val = raw_test_point[text_column + g.DECORUM]
                    if actual_val == 0:
                        exp_str += '' + g.EXP_SEP + ' {} has negative sentiments'.format(text_column)
                    else:
                        exp_str += '' + g.EXP_SEP + ' {} has positive sentiments'.format(text_column)
                elif type_of_text == g.RESOLUTION:
                    actual_val = raw_test_point[text_column + g.RESOLUTION]
                    if actual_val == 0:
                        exp_str += '' + g.EXP_SEP + ' {} doesn\'t seem to resolve issues or concerns'.format(
                            text_column)
                    else:
                        exp_str += '' + g.EXP_SEP + ' {} seems to resolve issues or concerns'.format(text_column)
                elif type_of_text == g.CEX:
                    actual_val = raw_test_point[text_column + g.CEX]
                    if actual_val == 0:
                        exp_str += '' + g.EXP_SEP + ' {} suggests an overall poor experience'.format(text_column)
                    else:
                        exp_str += '' + g.EXP_SEP + ' {} suggests an overall good experience'.format(text_column)
                elif type_of_text == g.SENTIMENT_SCORE:
                    filler = 'average sentiment is '
                    if actual_val >= 0.85:
                        filler += 'very positive'
                    elif actual_val < 0.85 and actual_val >= 0.70:
                        filler += 'positive'
                    elif actual_val < 0.70 and actual_val >= 0.501:
                        filler += 'slightly positive'
                    elif actual_val < 0.501 and actual_val >= 0.499:
                        filler += 'neutral'
                    elif actual_val < 0.499 and actual_val >= 0.35:
                        filler += 'slightly negative'
                    elif actual_val < 0.35 and actual_val >= 0.15:
                        filler += 'negative'
                    else:
                        filler += 'very negative'

                    if operator == '<=':
                        words_operator = 'that is less than '
                    else:
                        words_operator = 'that is more than '

                    exp_str += '' + g.EXP_SEP + ' {} {} ({}: {} {})'.format(text_column, filler, actual_val,
                                                                            words_operator, thresh)
                elif type_of_text == g.HASHED:
                    exp_str += '' + g.EXP_SEP + ' {} is {}'.format(text_column, raw_test_point[text_column])
                elif g.TOPICS_COLS in type_of_text:
                    # topic = col[col.rfind('_')+1:]
                    positive_words = []
                    negative_words = []
                    text_sentence = raw_test_point[text_column]
                    for topic_feat in feature_imp_dict:
                        if topic_feat.startswith(text_column + g.TOPICS_COLS):
                            word = topic_feat[topic_feat.rfind('_') + 1:]
                            if word.lower() in text_sentence.lower():
                                positive_words.append(word)
                            else:
                                negative_words.append(word)
                    if len(positive_words) != 0:
                        exp_str += '' + g.EXP_SEP + ' {} includes [ {} ]'.format(text_column,
                                                                                        ', '.join(positive_words))
                    if len(negative_words) != 0:
                        exp_str += '' + g.EXP_SEP + ' {} excludes [ {} ]'.format(text_column,
                                                                                                  ', '.join(
                                                                                                      negative_words))
                elif g.CONCEPT_COLS in type_of_text:
                    phrase = col[col.find('_derived_concept') + 17:].replace('_',
                                                                             ' ')  # This assumes that phrase doesn't have an underscore, so that's a todo
                    text_column = col.split(g.CONCEPT_COLS)[0]
                    text_sentence = str(raw_test_point[text_column]).lower()
                    if phrase.lower() not in text_sentence:
                        exp_str += '' + g.EXP_SEP + ' {} excludes the phrase {}'.format(text_column, phrase)
                    else:
                        exp_str += '' + g.EXP_SEP + ' {} includes the phrase {}'.format(text_column, phrase)
                else:
                    # Expectation is this will be of the form _derived_extremely_poor, _derived_positive etc. so we remove _derived_
                    type_of_text = type_of_text[9:]
                    if operator == '<=':
                        filler = 'does not have'
                        second_filler = 'that is less than or equal to'
                    else:
                        filler = 'has'
                        second_filler = 'that is more than or equal to'
                    exp_str += '' + g.EXP_SEP + ' The {} {} {} sentiments ({}: {} {})'.format(text_column, filler,
                                                                                              type_of_text.replace('_',
                                                                                                                   ' '),
                                                                                              actual_val, second_filler,
                                                                                              thresh)
        else:
            if col in global_info_dict and global_info_dict[col]['type'] == 'categorical' and operator == '==':
                exp_str += ' ' + g.EXP_SEP + ' {} is {} '.format(feature, actual_val)
            elif col in global_info_dict and global_info_dict[col]['type'] == 'categorical' and operator == '!=':
                category = global_info_dict[col]['col_name']
                if raw_test_point is not None:
                    try:
                        if from_pdf:
                            feature = feature + ' is ' + apply_unidecoding(
                                raw_test_point[category].iloc[0]).upper()
                        else:
                            feature = feature + ' is ' + apply_unidecoding(
                                raw_test_point[category]).upper()
                    except Exception as e:
                        feature = feature + ' is ' + str(raw_test_point[category]).upper()
                if '{' in thresh and ',' in thresh:  # Assuming the categories doesn't have these symbols when thresh takes the form {cat1, cat2}
                    exp_str += '' + g.EXP_SEP + ' {} (not equal to any of  {}) '.format(feature, thresh)
                else:
                    exp_str += '' + g.EXP_SEP + ' {} (not {}) '.format(feature, thresh)
            else:
                if operator == '<=':
                    words_operator = 'that is less than or equal to'
                elif operator == '>':
                    words_operator = 'that is more than'
                elif operator == '>=':
                    words_operator = 'that is more than or equal to'
                else:
                    words_operator = 'that is in range'
                exp_str += ' ' + g.EXP_SEP + ' {} is {} ({} {})'.format(feature, actual_val,
                                                                        words_operator,
                                                                        thresh)
    return exp_str


def predict_results_from_service(
        test_data, outcome, model_data, extra_info, proba=False):
    """
    :param test_data: Test data on which model should be predicted
    :param features: Features used to build model
    :param outcome_type: The data type of the outcome variable
    :param outcome_name: The name of the outcome variable
    :param model_selected_path: the path of the model acts as model id for the modelling service
    :return: predicted results
    """
    g = DotDict(extra_info["g"])
    features = extra_info[g.FEATURES_SELECTED]
    model_path = extra_info[g.MODEL_PATH]
    cat_types = None
    deviation_threshold = None
    radius_threshold = None
    sampled_population = None
    model_proba = proba            
    #loading model
    model = get_model_dictionary(model_path)
    scaler = model_data['scaler']
    std_dev = None
    stat_df = None
    prediction, prediction_prob = predict_sklearn(test_data, model, outcome, scaler,
                    proba=proba, std_dev=std_dev,
                    stat_df=stat_df, cat_types=cat_types, radius_threshold=radius_threshold,
                    sampled_population=sampled_population, deviation_threshold=deviation_threshold)
    if not proba:
        return np.array(prediction)
    else:
        return np.array(prediction_prob)


def predict_sklearn(test_data, model, outcome, scaler_path,
                    is_classification=True, proba=False, std_dev=None,
                    stat_df=None, cat_types=None, radius_threshold=0.3,
                    sampled_population=40, deviation_threshold=0.07):
    
    if outcome in test_data.columns:
        test_data = test_data.drop(outcome, axis=1)
    if scaler_path is not None:
        scaler = get_model_dictionary(scaler_path) 
        test_data = pd.DataFrame(data=scaler.transform(test_data), columns=test_data.columns)
    
    if not is_classification:
        predicted = model.predict(test_data)
        predicted = map(float, predicted)
        predicted_prob = None
    else:
        if proba:
            predicted_prob = model.predict_proba(test_data)    
            predicted = model.predict(test_data)
            pd.np.random.seed(42)
            random.seed(42)
            if std_dev is not None:
                if std_dev <= deviation_threshold:
                    le = sk_pr.LabelEncoder()
                    label_len = len(predicted_prob[0])
                    max_indices = [
                        list(lst).index(max(lst)) for lst in predicted_prob]
                    if scaler_path is not None:
                        test_data = pd.DataFrame(data=scaler.inverse_transform(
                            test_data), columns=test_data.columns)
                    col_dict = {}
                    test_data_new = test_data.copy()
                    cat_type_list = []
                    for key, value_list in cat_types.items():
                        col_list = []
                        for col in test_data.columns: 
                            if key in col and col.replace(
                                key+"_", "") in value_list:
                                if key not in cat_type_list:
                                    cat_type_list.append(key)
                                col_list.append(col)
                                test_data_new = test_data_new.drop(col, axis=1)
                        if len(col_list) > 0:
                            col_dict[key] = col_list
                    for key, value_list in col_dict.items():
                        df_append = test_data[value_list]
                        test_data_new[key] = df_append.apply(
                            lambda row: get_original(
                            df_append, row, key, cat_types[key]), axis=1)
                    feat_len = len(test_data_new.columns)
                    predicted_prob = []
                    for ind, test_sample in test_data_new.iterrows():
                        near_generated_points = pd.DataFrame(
                            columns=test_data_new.columns)
                        for ind1, col in enumerate(test_data_new.columns):
                            if col in cat_types.keys():
                                cat_types_list = le.fit_transform(
                                    cat_types[col])
                                if test_sample[col] == None:
                                    test_sample[col] = "NULL"
                                test_value = le.transform(
                                    [test_sample[col]])[0]
                                min_value = min(cat_types_list)
                                max_value = max(cat_types_list)
                            else:
                                min_value = stat_df[0][col]
                                max_value = stat_df[1][col]
                                test_value = test_sample[col]
                            population = [random.uniform(max(test_value-0.17*(
                                max_value-min_value),
                                min_value), min(test_value+0.17*(
                                max_value-min_value), max_value
                                )) for _ in range(sampled_population)]
                            if col in cat_types.keys():
                                population = [int(math.floor(
                                    i)) if i<test_value else int(math.ceil(
                                    i)) for i in population]
                                population = le.inverse_transform(population)
                                near_generated_points[col] = population
                            else:
                                near_generated_points[col] = population
                        generated_points = near_generated_points.copy()
                        generated_points = pd.get_dummies(generated_points,
                            columns=cat_type_list, dummy_na=False,
                            prefix=cat_type_list, prefix_sep="_")
                        if generated_points.columns.duplicated().any():
                            generated_points = generated_points.loc[
                                :, ~generated_points.columns.duplicated()]
                        for col in test_data.columns:
                            if col not in generated_points.columns:
                                generated_points[col] = 0
                        generated_points = generated_points[test_data.columns]
                        near_generated_points = generated_points.to_numpy()
                        if scaler_path is not None:
                            near_generated_points = pd.DataFrame(
                                data=scaler.transform(near_generated_points),
                                columns=test_data.columns)
                        pred_on_points = model.predict(near_generated_points)
                        count = 0
                        for pred_on_point in pred_on_points:
                            if pred_on_point == predicted[ind]:
                                count += 1
                        pred_score = round(max(float(count)/sampled_population,
                            1-(float(count)/sampled_population)), 2)
                        max_ind = max_indices[ind]
                        pred_score_list = []
                        for label_ind in range(label_len):
                            if label_ind == max_ind:
                                pred_score_list.append(pred_score)
                            else:
                                pred_score_list.append(
                                    float(1-pred_score)/(label_len-1))
                        predicted_prob.append(pred_score_list)
            predicted_prob = np.array(predicted_prob)
        else:
            predicted = model.predict(test_data)
            predicted_prob = None
    return predicted, predicted_prob