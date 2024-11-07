"""Extract data insights from classification datasets

This script allows the user to extract significant rules from the dataset.

To use this,

import it as a module and call get_top_explanations from this script and
pass the input dataframe and the outcome dataframe

"""
import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from collections import OrderedDict

g = None
OUTLIER_SENSITIVITY=1


def find_outliers(data): # this takes all the columns
    model = IsolationForest(n_estimators=50,
                            max_samples=256,
                            random_state=42,
                            # n_jobs=1,
                            contamination='auto'
                           )
    model.fit(data)
    scores = model.decision_function(data)
    counts, thresholds = np.histogram(scores, bins='auto')
    out_thresh = -1  #default value
    count_list = list(counts)
    if 0 in counts:
        start_idx = count_list.index(0)
        end_idx = min(start_idx + OUTLIER_SENSITIVITY, len(count_list))
        if count_list[start_idx:end_idx].count(0) == OUTLIER_SENSITIVITY:
            idx = list(counts).index(0)
            left_sum = sum(counts[:idx])
            if left_sum / float(sum(counts)) < 0.1:
                out_thresh = thresholds[idx]
    data = pd.DataFrame(data)
    return data[scores < out_thresh].index.tolist()


def penalizing_scores(p_hat, tot_count, scores, mode="DI"):
    '''
    Give penalty to the scores based on their b/p_hat value.
    If b/p_hat is more then penalty will be more.

    Args:
    p_hat: It is the multiplication of accuracy and coverage of each node.
    tot_count: Total count of each node.
    scores: Calulated confidence score of each node.
    mode: It will be "LE" for Local Explanation and "DI" for Data Insights.

    Returns:
    scores: Scores of each node after penalty.
    b: Confidence interval estimator of original probability.
    penalty: The b/p_hat value of each node. On the basis of this
    we gives the penalty to the scores of each node.
    '''
    z_alpha = 1.16
    b = 2 * z_alpha * np.sqrt(p_hat * (1 - p_hat) / tot_count[0])
    penalty = b / p_hat
    penalty_factor = []
    if mode == "LE":
        if type(penalty) != type(np.array([])):
            penalty = np.array([penalty])
            scores = np.array([scores])
    penalties = OrderedDict([(0.1, 1), (0.2, 0.99), (0.3, 0.97), (0.4, 0.92),
                             (0.5, 0.90), (">0.5", 0.88)])
    if mode == "DI" and g.AUGI_PHAT_USER_PENALTY is True:
        penalties = OrderedDict([(0.1, g.AUGI_B_PHAT_BPS_01),
                                 (0.2, g.AUGI_B_PHAT_BPS_02),
                                 (0.3, g.AUGI_B_PHAT_BPS_03),
                                 (0.4, g.AUGI_B_PHAT_BPS_04),
                                 (0.5, g.AUGI_B_PHAT_BPS_05),
                                 (">0.5", g.AUGI_B_PHAT_BPS_05_PLUS)])

    for idx in range(len(scores)):
        if penalty[idx] < list(penalties.keys())[0]:
            scores[idx] = scores[idx] * list(penalties.values())[0]
            penalty_factor.append(list(penalties.values())[0])

        elif penalty[idx] < list(penalties.keys())[1]:
            scores[idx] = scores[idx] * list(penalties.values())[1]
            penalty_factor.append(list(penalties.values())[1])

        elif penalty[idx] < list(penalties.keys())[2]:
            scores[idx] = scores[idx] * list(penalties.values())[2]
            penalty_factor.append(list(penalties.values())[2])

        elif penalty[idx] < list(penalties.keys())[3]:
            scores[idx] = scores[idx] * list(penalties.values())[3]
            penalty_factor.append(list(penalties.values())[3])

        elif penalty[idx] < list(penalties.keys())[4]:
            scores[idx] = scores[idx] * list(penalties.values())[4]
            penalty_factor.append(list(penalties.values())[4])

        else:
            scores[idx] = scores[idx] * list(penalties.values())[5]
            penalty_factor.append(list(penalties.values())[5])
    return scores, b, penalty, penalty_factor


def calculate_sigmoid(alpha, beta, ip_val):
    return (1 / (1 + np.exp(-(ip_val - alpha) * beta)))


# local explanations vs data-insights have different parameters for scoring
# parameter mode specifies which one of the two applications needs calculation
def alpha_beta_cal(mode, data_df):
    q = [
        0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7,
        0.75, 0.8, 0.85, 0.9, 0.95
    ]
    target_col = [
        0.4, 0.43, 0.45, 0.48, 0.5, 0.6, 0.65, 0.67, 0.7, 0.75, 0.78, 0.8,
        0.85, 0.87, 0.9, 0.93, 0.95, 0.99
    ]

    m = ['Accuracy', 'Coverage']
    q_df = data_df[m].quantile(q)

    # The accuracy below 55% is poor, while the coverage above 5% is good.

    if mode == 'LE':
        acc_alpha = min(0.55, q_df['Accuracy'].iloc[5])
        cov_alpha = q_df['Coverage'].iloc[4]
    else:
        acc_alpha = min(0.59, q_df['Accuracy'].iloc[5])
        cov_alpha = q_df['Coverage'].iloc[4]

    acc_beta = []
    cov_beta = []
    for i in range(len(q_df)):
        if (q_df['Accuracy'].iloc[i] - acc_alpha) != 0:
            acc_beta.append(
                abs(target_col[i] / (q_df['Accuracy'].iloc[i] - acc_alpha)))
        else:
            acc_beta.append(0)

        if (q_df['Coverage'].iloc[i] - cov_alpha) != 0:
            cov_beta.append(
                abs(target_col[i] / (q_df['Coverage'].iloc[i] - cov_alpha)))
        else:
            cov_beta.append(0)

    if mode == 'LE':
        acc_beta = max(min(10, np.mean(acc_beta) * 3), 8)
        cov_beta = max(min(70, np.mean(cov_beta)), 40)
    else:
        acc_beta = max(min(12, np.mean(acc_beta) * 3), 10)
        cov_beta = max(min(70, np.mean(cov_beta)), 30)

    # print('Alpha_accuracy- {}, Alpha_coverage- {}'.
    #                         format(acc_alpha,cov_alpha))
    # print('Beta_accuracy- {}, Beta_coverage- {}\n'.
    #                         format(acc_beta,cov_beta))

    # TODO do the following if debug mode is enabled
    q_df['S_Accuracy'] = calculate_sigmoid(acc_alpha, acc_beta,
                                           q_df['Accuracy'])
    q_df['S_Coverage'] = calculate_sigmoid(cov_alpha, cov_beta,
                                           q_df['Coverage'])

    q_df['Confidence'] = q_df['S_Accuracy'] * q_df['S_Coverage']
    if g.DI_DEBUG_MODE:
        utility.dbglog(("(alpha, beta) for accuracy, coverage:",
                       (acc_alpha, acc_beta), (cov_alpha, cov_beta)))
        utility.dbglog(("q_df", q_df))

    return acc_alpha, acc_beta, cov_alpha, cov_beta


def scoring_model_sigmoid(mode, accuracy, coverage, sig_th_tuple=None):
    if not sig_th_tuple:
        data = pd.DataFrame(list(zip(accuracy, coverage)),
                            columns=['Accuracy', 'Coverage'])
        acc_alpha, acc_beta, cov_alpha, cov_beta = alpha_beta_cal(mode, data)
    else:
        acc_alpha, acc_beta, cov_alpha, cov_beta = sig_th_tuple
    if mode == "DI" and g.AUGI_USER_SCORE is True:
        if g.AUGI_ALPHA_ACC and (g.AUGI_ALPHA_ACC != 0.0):
            acc_alpha = g.AUGI_ALPHA_ACC
        if g.AUGI_BETA_ACC and (g.AUGI_BETA_ACC != 0.0):
            acc_beta = g.AUGI_BETA_ACC
        if g.AUGI_ALPHA_COV and (g.AUGI_ALPHA_COV != 0.0):
            cov_alpha = g.AUGI_ALPHA_COV
        if g.AUGI_BETA_COV and (g.AUGI_BETA_COV != 0.0):
            cov_beta = g.AUGI_BETA_COV

    s_coverage = calculate_sigmoid(cov_alpha, cov_beta, coverage)
    if g.AUGI_INFLATE_ACCURACY_SCORE:
        s_accuracy = calculate_sigmoid(acc_alpha, acc_beta, accuracy)
    else:
        s_accuracy = accuracy

    confidence = np.vectorize(lambda i: min(i, 0.98))(s_accuracy * s_coverage)
    if g.DI_DEBUG_MODE and (not sig_th_tuple):
        df_debug = np.c_[accuracy, coverage, s_accuracy, s_coverage,
                         confidence]
        for x, y, sx, sy, z in df_debug:
            utility.dbglog(('ACCURACY, COVERAGE, SCORE, FINAL SCORE', x, sx, y,
                            sy, sx * sy, z))
    return confidence, (acc_alpha, acc_beta, cov_alpha,
                        cov_beta), s_coverage, s_accuracy


def get_knee_threshold(values,
                       relaxation_angle=10,
                       min_sample=1,
                       return_index=False, mode="classification"):
    thresh = get_knee_threshold_core(values, relaxation_angle, min_sample,
                                     return_index)

    # Let's cap the knee of the curve on both ends (high/low)till we find out
    # the RCA for knee failures, user perception of scores is usually modeled
    # after american school grading system - below 60% is fail anyways.
    # TODO: this should be configurable
    if g.DI_DEBUG_MODE:
        utility.dbglog(("Original knee= ", thresh))
    if mode == "classification":
        return min(max(thresh, g.AUGI_KN_THRESHOLD_MIN_CLASSIF),
                   g.AUGI_KN_THRESHOLD_MAX_CLASSIF)
    else:
        return min(max(thresh, g.AUGI_KN_THRESHOLD_MIN_REGR),
                   g.AUGI_KN_THRESHOLD_MAX_REGR)

def get_knee_threshold_core(values,
                            relaxation_angle=10,
                            min_sample=1,
                            return_index=False):
    """Uses Knee of the curve method on the values array and computes the
    threshold which corresponds to the kth smallest element present in the
    array. This is useful when you have an array of values and want to find
    a monotonic median
    Args:
        values (list): Array of values (sorted or otherwise) on which Knee of
            the curve will be computed. Must contain atleast four elements.
        relaxation_angle (int, optional): Adjust the threshold to be more
            lenient if it's strict. Defaults to 10. Must be in range [0, 90]
        min_sample (int, optional): The minimum number of values to consider
            to the left of the knee irrespective of the relaxation_angle.
            Defaults to 1.
        return_index (bool, optional): Return the k of the kth smallest element
            present in the array instead of the kth smallest element itself.
            Defaults to False.

    Returns:
        int: kth smallest element of the array or it's index depending on
            return_index is set to False or True.
    """
    if not isinstance(values, list) and not isinstance(values, np.ndarray):
        raise TypeError("values must be a list or np.ndarray")

    if not isinstance(relaxation_angle, numbers.Real):
        raise TypeError("relaxation_angle must be a real number")

    if not isinstance(min_sample, numbers.Integral):
        raise TypeError("min_sample must be an integer")

    if relaxation_angle < 0 or relaxation_angle > 90:
        raise ValueError("relaxation_angle must be in the range [0, 90]")

    # Typecast list to np.ndarray
    if isinstance(values, list):
        values = np.array(values)

    if len(values.shape) >= 2:
        raise ValueError("Only one dimensional array is allowed")

    if isinstance(values, np.ndarray) and values.size <= 3:
        # raise ValueError("Values must contain a minimum
        #     number of four elements")
        return 0.0

    # Compute knee using scores between [0.6, 0.9]
    if values[np.logical_and(g.MIN_SCORES <= values,
                             values <= g.MAX_SCORES)].shape[0] > 3:
        values = values[np.logical_and(g.MIN_SCORES <= values,
                                       values <= g.MAX_SCORES)]
        if g.DI_DEBUG_MODE:
            utility.dbglog(("Subset of scores- ", values.shape, values))

    # append the values with it's indices
    pts = np.c_[np.arange(values.size, dtype=int), values]
    pts = np.array(sorted(pts, key=lambda x: x[1]))

    # Compute the convex hull of the points and extract critical points
    # Uses quick hull algorithm and average time complexity is O(nlogn)
    # Convex hull approximately computes the polynomial required to fit
    # the points
    try:
        ch = ConvexHull(pts)
        hull_indices = ch.vertices
    except Exception as e:
        traceback.print_exc()
        hull_indices = np.arange(pts.shape[0], dtype=np.int)
    hull_pts = pts[hull_indices]

    # This we do because the output from the convex hull does not
    # maintain the order.
    hull_pts = sorted(pts[hull_indices], key=lambda x: x[1])

    # Knee of the curve method
    if hull_indices.shape[0] != pts.shape[0]:
        dist = pts[:, 1][ch.simplices]
        counts, thresh = np.histogram(np.abs(dist[:, 1] - dist[:, 0]),
                                      bins='auto')
        reference_point = np.sort(ch.simplices[np.where(
            np.abs(dist[:, 1] - dist[:, 0]) > thresh[-2])[0]][0])
        reference_line = pts[reference_point[0]] - pts[reference_point[1]]
        hull_indices = np.arange(pts.shape[0], dtype=np.int)
        hull_pts = pts[hull_indices]
        hull_pts = sorted(pts[hull_indices], key=lambda x: x[1])
    else:
        reference_point = [0, pts.shape[0] - 1]
        reference_line = pts[-1] - pts[0]

    if reference_point[0] + 1 == reference_point[1]:
        return 0.5 * hull_pts[reference_point[0]][1] + 0.5 * hull_pts[
            reference_point[1]][1]

    # utility.dbglog(('RANGE: ',  range(reference_point[0]+1,
    #     reference_point[1])))
    # utility.dbglog(('pts: ',pts))
    norm_reference_line = np.linalg.norm(reference_line)
    normal_dist = [
        np.linalg.norm(
            np.cross(reference_line, pts[reference_point[0]] - pts[x])) /
        norm_reference_line
        for x in range(reference_point[0] + 1, reference_point[1])
    ]
    base_threshold_hull_index = np.argmax(normal_dist) + reference_point[0] + 1

    # Relaxation of the threshold computed by the knee of the curve
    angle = 0
    threshold_hull_index = base_threshold_hull_index - 1

    while (threshold_hull_index >= 0
           and hull_pts[threshold_hull_index][1] > min_sample
           and angle < relaxation_angle):

        # line segment will originate from the point left to the max distance
        # point (distance relative to reference line)
        line_segment = (hull_pts[base_threshold_hull_index] -
                        hull_pts[threshold_hull_index])
        norm_line_segment = np.linalg.norm(line_segment)

        dot_product = np.sum(line_segment * reference_line)
        angle = np.arccos(
            dot_product /
            (norm_line_segment * norm_reference_line)) * (180 / np.pi)
        threshold_hull_index -= 1

    if return_index:
        # Returns the index of the computed threshold
        return hull_pts[threshold_hull_index +
                        1][0]  # TODO: TO FIX THIS AND TEST
    # Returns the kth largest element present in the values array where
    # k is the computed threshold.
    return hull_pts[threshold_hull_index + 1][1]


def build_tree(X, y, min_sample_split=1, criterion="entropy",
               type="classification"):
    """Builds the decision tree given the dataset

    Args:
        X (pd.DataFrame): Pandas dataframe containing the data
        y (pd.DataFrame): Pandas dataframe containing the outcome column
            of the dataset
        min_sample_split (int): the minimum number of samples required for
            a node to be considered as a leaf
        criterion (str, optional): the criterion of the decision tree.
            Should be either "gini" or "entropy". Defaults to "entropy".

    Returns:
        [DecisionTreeClassifier]: The fitted decision tree classifier
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame")
    if not isinstance(y, pd.DataFrame) and not isinstance(y, pd.Series):
        raise TypeError("y must be a pandas DataFrame")
    if len(X.columns) < 1:
        raise ValueError("Atleast two columns are required")
    if len(y.unique()) == 1:
        raise ValueError("Atleast two class labels are required")
    sum_uniq = 0
    for col in X.columns:
        sum_uniq += X[col].nunique()
    if sum_uniq == len(X.columns):
        raise ValueError("Atleast two labels are required in any column of X")
    if not isinstance(min_sample_split, numbers.Integral):
        raise TypeError("min_sample_split must be an integer")
    if min_sample_split < 0:
        raise ValueError("min_sample_split must be greater than 0")
    if not isinstance(type, str):
        raise TypeError("type must be a string")
    if type not in ["classification", "regression"]:
        raise ValueError("type must be one of [classification, regression']")
    if type == 'classification':
        if criterion not in ["gini", "entropy"]:
            raise ValueError("criterion must be one of [gini, entropy]")
        else:
            # TODO: should this also be hard-coded to some value e.g. 5
            # what if there are too many classes e.g. 25 or 50?
            # class_weight = balance was added to add a bug fix where data
            # was biased for one class e.g. for one class number of points is
            # 4% while for other its 96%.
            if g.AUGI_CLASS_BALANCE:
                class_weight_param = 'balanced'
            else:
                # Give default value of class_weight
                class_weight_param = None
            clf = DecisionTreeClassifier(criterion=criterion,
                                         max_depth=16,
                                         random_state=0,
                                         class_weight=class_weight_param)
            rf = RandomForestClassifier(criterion=criterion,
                                        max_depth=16,
                                        random_state=0,
                                        n_estimators=g.AUGI_N_MODELS,
                                        bootstrap=False,
                                        class_weight=class_weight_param)
    if type == 'regression':
        if criterion != 'mse':
            raise ValueError("criterion can only be mse")
        else:
            # TODO: should this also be hard-coded to some value e.g. 5
            clf = DecisionTreeRegressor(criterion=criterion,
                                        max_depth=16,
                                        random_state=0)
            rf = RandomForestRegressor(criterion=criterion,
                                       max_depth=16,
                                       random_state=0,
                                       n_estimators=g.AUGI_N_MODELS,
                                       bootstrap=False)
    try:
        clf.fit(X, y)
        rf.fit(X, y)
    except:
        traceback.print_exc()
        raise Exception("Tree could not be built")
    # Consider both random forest with sqrt(p) predictors and decision tree
    # with all p predictors
    trees = rf.estimators_ + [clf]
    pruned_nodes = []
    try:
        for i in range(0, len(trees)):
            tree_copy = deepcopy(trees[i])
            if g.DI_DEBUG_MODE:
                if not os.path.exists(config.AUGI_TREES_PATH):
                    os.mkdir(config.AUGI_TREES_PATH)
                if type == 'classification':
                    out_file = config.AUGI_TREES_PATH + 'classif_unpruned' + str(i) + '.dot'
                    export_graphviz(tree_copy,
                                    out_file,
                                    feature_names=X.columns.tolist(),
                                    class_names=rf.classes_.astype(str),
                                    node_ids=True)
                    (graph,) = pydot.graph_from_dot_file(out_file)
                    graph.write_png(config.AUGI_TREES_PATH + 'classif_unpruned' +
                                    str(i) + '.png')

                else:
                    out_file = config.AUGI_TREES_PATH + 'regr_unpruned' + str(i) + '.dot'
                    export_graphviz(tree_copy,
                                    out_file,
                                    feature_names=X.columns.tolist(),
                                    node_ids=True)
                    (graph,) = pydot.graph_from_dot_file(out_file)
                    graph.write_png(config.AUGI_TREES_PATH + 'regr_unpruned' +
                                    str(i) + '.png')
            if g.ENABLE_FAST_PRUNING:
                distribution, nodes_leaves = get_distribution(tree_copy, X, y)
                pruned_nodes.append(
                    prune(tree_copy,
                          X,
                          y,
                          type,
                          distribution,
                          nodes_leaves,
                          debug=g.DI_DEBUG_MODE,
                          local_g=g,
                          tree_num=i, source="DI"))
                trees[i].pruned_nodes = pruned_nodes[i]
                if g.DI_DEBUG_MODE:
                    if type == 'classification':
                        out_file = config.AUGI_TREES_PATH + 'classif_pruned' + str(i) + '.dot'
                        export_graphviz(tree_copy,
                                        out_file,
                                        feature_names=X.columns.tolist(),
                                        class_names=rf.classes_.astype(str),
                                        node_ids=True)
                        (graph,) = pydot.graph_from_dot_file(out_file)
                        graph.write_png(config.AUGI_TREES_PATH + 'classif_pruned' +
                                        str(i) + '.png')
                    else:
                        out_file = config.AUGI_TREES_PATH + 'regr_pruned' + str(i) + '.dot'
                        export_graphviz(tree_copy,
                                        out_file,
                                        feature_names=X.columns.tolist(),
                                        node_ids=True)
                        (graph,) = pydot.graph_from_dot_file(out_file)
                        graph.write_png(config.AUGI_TREES_PATH + 'regr_pruned' +
                                        str(i) + '.png')
    except Exception as e:
        traceback.print_exc()
        raise e

    utility.dbglog(('The pruned nodes are as follows', pruned_nodes))
    # Debugging aid: pickle dump and tree visuals dump
    if g.DI_DEBUG_MODE:
        pickle.dump((X, y, clf, rf), open('rfclf.pkl', 'wb'))
        folder_name = "augi_debug_dump_" + datetime.datetime.now().strftime(
            "%Y%m%d%H%M%S") + "/"
        os.mkdir(folder_name)
        # TODO get rid of the first condition here
        if type == 'classification':
            for i, tree in enumerate(trees):
                export_graphviz(tree,
                                out_file=folder_name + 'classif' + str(i) +
                                '.dot',
                                feature_names=X.columns.tolist(),
                                class_names=rf.classes_.astype(str),
                                node_ids=True)
                pickle.dump((X, y, i, tree),
                            open(folder_name + 'classif' + str(i) + '.pkl',
                                 'wb'))
        else:
            for i, tree in enumerate(trees):
                export_graphviz(tree,
                                feature_names=X.columns.tolist(),
                                node_ids=True,
                                out_file=folder_name + 'regr' + str(i) +
                                '.dot')
                pickle.dump((X, y, i, tree),
                            open(folder_name + 'regr' + str(i) + '.pkl', 'wb'))
    return trees


# get scores for debugging aid for every class, returns a vector
def get_node_score(prevnode, value, clf, sig_th_tuple, dtree_inflate):
    node_score = []
    value = np.squeeze(value)
    for idx_class, idx_count in enumerate(value):
        tot_count = np.sum(value)
        confidence = idx_count / tot_count
        coverage = tot_count / np.sum(np.squeeze(clf.tree_.value[0]))
        if not g.AUGI_SIGMOID_SCORING:
            inflated_cov = dtree_inflate.predict(
                np.array(coverage).reshape(-1, 1))
            scores = np.vectorize(lambda i: min(i, 0.98))(inflated_cov *
                                                          confidence)
        else:
            scores, _, _, _ = scoring_model_sigmoid('DI', confidence, coverage,
                                                    sig_th_tuple)
            scores = scores.tolist()
        node_score.append((round(scores,
                                 2), idx_class, int(idx_count), int(tot_count),
                           round(confidence, 2), round(coverage, 2), prevnode))
    return node_score


def get_rules(dtc,
              feature_names=None,
              min_confidence=0.92,
              leaf_strength=8,
              knee_method=False,
              is_clf=False,
              sig_th_tuple=None,
              rule_lime=None,
              dtree_inflate=None):
    """Given the decision tree and feature names, extract
    the rules and the class distribution along it's path

    Args:
        dtc (DecisionTreeClassifier): Sklearn's decision tree classifier
        feature_names (list, optional): List of feature names. Defaults to None
        min_confidence (float, optional): The minimum confidence of the node
            required. Defaults to 0.92.
        leaf_strength (int, optional): The minimum leaf strength of the node
            required. Defaults to 8.
        knee_method (bool, optional): Whether to use knee method or not.
            Defaults to False.
        Defaults override leaf_strength and min_confidence as they are
            determined automatically by knee_method

    Returns:
        [tuple]: Either three tuple or two tuple containing rule list,
            values path and the determined quality score. This quality score
            tells us how much the rule explains the predicted class label.
    """
    rules_list = []
    values_path = []
    values = dtc.tree_.value
    if rule_lime is not None:
        feat_class_dict = dict()
        for col in rule_lime['ginfodict']:
            if rule_lime['ginfodict'][col]['type'] == 'categorical':
                if rule_lime['ginfodict'][col][
                        'col_name'] not in feat_class_dict:
                    feat_class_dict[rule_lime['ginfodict'][col]
                                    ['col_name']] = [
                                        rule_lime['ginfodict'][col]['category']
                                    ]
                else:
                    feat_class_dict[
                        rule_lime['ginfodict'][col]['col_name']].append(
                            rule_lime['ginfodict'][col]['category'])
        if g.DI_DEBUG_MODE:
            utility.dbglog((feat_class_dict, 'FEAT_CLASS_DICT'))

    def RevTraverseTree(tree, node, rules, pathValues, dtc, sig_th_tuple,
                        trav_dict, dtree_inflate):
        """
        Traverase an skl decision tree from a node (presumably a leaf node)
        up to the top, building the decision rules. The rules should be
        input as an empty list, which will be modified in place. The result
        is a nested list of tuples: (feature, direction (left=-1), threshold).
        The "tree" is a nested list of simplified tree attributes:
        [split feature, split threshold, left node, right node]
        """
        # now find the node as either a left or right child of something
        # first try to find it as a left node

        if node in trav_dict:
            rules.extend(trav_dict[node][0])
            pathValues.extend(trav_dict[node][1])
            return
        try:
            prevnode = tree[2].index(node)
            leftright = "<="
            pathValues.append(values[prevnode])
        except ValueError:
            # failed, so find it as a right node - if this also causes an
            # exception, something's really messed up
            prevnode = tree[3].index(node)
            leftright = ">"
            pathValues.append(values[prevnode])

        # now let's get the rule that caused prevnode to -> node
        p1 = feature_names[tree[0][prevnode]]
        p2 = tree[1][prevnode]
        if rule_lime is not None:
            if p1 in rule_lime['ginfodict']:
                if rule_lime['ginfodict'][p1]['type'] == 'categorical':
                    if leftright == '<=':
                        parent_categ = rule_lime['ginfodict'][p1]['col_name']
                        class_labels = feat_class_dict[parent_categ]
                        curr_categ = rule_lime['ginfodict'][p1]['category']
                        if len(class_labels) == 2:
                            desired_categ = 1 - class_labels.index(curr_categ)
                            p1 = parent_categ + '_' + class_labels[
                                desired_categ]
                            leftright = '>'

        if g.DI_DEBUG_MODE:
            if is_clf:
                node_score = get_node_score(prevnode, values[prevnode], dtc,
                                            sig_th_tuple, dtree_inflate)
            else:
                node_score = get_regression_node_score(prevnode,
                                                       values[prevnode], dtc,
                                                       sig_th_tuple,
                                                       dtree_inflate)
            rule_filter = " (X['" + str(p1) + "'] " + leftright + " " + str(
                p2) + ") "
            rules.append(
                (node_score, str(p1) + " " + leftright + " " + str(p2),
                 rule_filter))
        else:
            rules.append(str(p1) + " " + leftright + " " + str(p2))

        # if we've not yet reached the top, go up the tree one more step
        if prevnode != 0:
            RevTraverseTree(tree, prevnode, rules, pathValues, dtc,
                            sig_th_tuple, trav_dict, dtree_inflate)
        trav_dict[node] = (rules, pathValues)

    leaves = np.arange(0, dtc.tree_.node_count)[1:]

    # build a simpler tree as a nested list:
    # [split feature, split threshold, left node, right node]
    thistree = [dtc.tree_.feature.tolist()]
    thistree.append(dtc.tree_.threshold.tolist())
    thistree.append(dtc.tree_.children_left.tolist())
    thistree.append(dtc.tree_.children_right.tolist())
    trav_dict = {}
    # get the decision rules for each leaf node & apply them
    for (_, nod) in enumerate(leaves):

        # get the decision rules
        rules = []
        pathValues = []

        RevTraverseTree(thistree, nod, rules, pathValues, dtc, sig_th_tuple,
                        trav_dict, dtree_inflate)

        pathValues.insert(0, values[nod])
        pathValues = list(reversed(pathValues))
        rules = list(reversed(rules))
        rules_list.append(rules)
        values_path.append(pathValues)
    return (rules_list, values_path)


def refine_explanation(explanation_list, avoid_extreme_thresholds=False):
    """Given a list of explanation of the format feature_name operator
    threshold, refines the explanation by sumarizing the thresholds.

    Args:
        explanation_list (list of str): List of explanations in string format.
        avoid_extreme_thresholds: (Bool): If set to true, it will just keep
            the threshold it encounters the first time in the path else it
            will keep the most recent threshold

    Returns:
        list of str: List of explanations in string format with condensed rules
    """
    if not isinstance(explanation_list, list):
        raise TypeError("feature_names must be a list")
    if not all(isinstance(x, str) for x in explanation_list):
        raise TypeError("feature_names should be a list of strings")
    seen_list = []
    double_seen_list = []
    explanation_list_filtered = []
    thresh_dict = dict()
    feat_op_dict = dict()
    for explanation in explanation_list:
        explanation = str(explanation)
        explanation = explanation.replace(">=", ">")
        if "<=" not in explanation:
            explanation = explanation.replace("<", "<=")
        if ("<=" not in explanation and ">" not in explanation
                and ">=" not in explanation):
            explanation_list_filtered.append(explanation)
            continue
        if "<=" in explanation:
            split_char = "<="
        else:
            split_char = ">"
        explanation = explanation.strip()
        feature, threshold = explanation.rsplit(split_char, 1)
        if feature not in seen_list and feature not in double_seen_list:
            explanation_list_filtered.append(explanation)
            seen_list.append(feature)
            feat_op_dict[feature] = split_char
            thresh_dict[feature] = [
                split_char,
                threshold,
                len(explanation_list_filtered),
            ]
        else:
            if feature not in double_seen_list or not avoid_extreme_thresholds:
                prev_split_char, prev_threshold, prev_pos = thresh_dict[
                    feature]
                # Update the interval with the latest threshold if
                # avoid_extreme_thresholds is false
                if isinstance(prev_threshold, list):
                    left, right = thresh_dict[feature][1]
                    if split_char == "<=":
                        right = min(float(threshold), float(right))
                    else:
                        left = max(float(threshold), float(left))
                    new_explanation = (
                        feature + " in " +
                        "( {0}, {1} )".format(str(round(float(left), 2)),
                                              str(round(float(right), 2))))
                    explanation_list_filtered[prev_pos - 1] = new_explanation
                    thresh_dict[feature][1] = [left, right]
                    continue
                elif (prev_split_char != split_char and
                      threshold != prev_threshold):
                    # This means the prev_threshold is integer and the
                    # split_char doesn't match.
                    # This means we need to generate an interval
                    left = min(prev_threshold, threshold)
                    right = max(prev_threshold, threshold)
                    if float(right) < float(left):
                        left, right = right, left
                    new_explanation = (
                        feature + " in " +
                        "( {0}, {1} )".format(str(round(float(left), 2)),
                                              str(round(float(right), 2))))
                    explanation_list_filtered[prev_pos - 1] = new_explanation
                    double_seen_list.append(feature)
                if not avoid_extreme_thresholds:
                    if threshold == prev_threshold:
                        continue
                    if prev_split_char == split_char:
                        explanation_list_filtered[prev_pos - 1] = explanation
                        thresh_dict[feature][1] = threshold
                    else:
                        thresh_dict[feature][1] = [left, right]
            continue
    return explanation_list_filtered, seen_list, feat_op_dict


def change_explanation(explanation, all_var_types):
    """Given a explanation string, converts it to more human readable format
    Args:
        explanation (str): A explanation string of the form feature operator
            threshold.
    Returns:
        [str]: Explanation string in more human readable format
    """
    if not isinstance(explanation, str):
        raise TypeError("explanation must be like a string")
    explanation = str(explanation)
    explanation = explanation.replace(">=", ">")
    if "<=" not in explanation:
        explanation = explanation.replace("<", "<=")
    if (
        " <= " not in explanation
        and " > " not in explanation
        and "==" not in explanation
    ):
        split_char = " in "
        feature, threshold = explanation.rsplit(split_char, 1)
        if feature.strip().endswith('_secs'):
            ft_name = feature[:feature.rfind("_")]
            datetime_types = all_var_types.loc[all_var_types[
                g.DATA_TYPE] == g.DT_DATETIME][g.VARIABLE_NAME].tolist()
            if ft_name in datetime_types:
                threshold = threshold.strip()
                number_1, number_2 = threshold[1:-1].split(',')
                number_1 = str(
                    datetime.timedelta(seconds=int(float(number_1))))
                number_2 = str(
                    datetime.timedelta(seconds=int(float(number_2))))
                threshold = '(' + str(number_1) + ', ' + str(number_2) + ')'
                feature = ft_name + '_time'
                explanation = feature + split_char + threshold
                return explanation
        type_of_text = feature[feature.rfind('_derived_'):].strip()
        if type_of_text and type_of_text.strip() == g.SENTIMENT_SCORE:
            expl = fix_text_cols(type_of_text.strip(), feature.strip(),
                                 split_char, threshold.strip())
            if expl is not None:
                return expl
        return explanation
    if " <= " in explanation:
        split_char = "<="
    else:
        split_char = ">"
    if "==" in explanation:
        feature_name, class_categ = explanation.rsplit("==", 1)
        if g.DI_DEBUG_MODE:
            explanation = feature_name + " is " + class_categ
        else:
            explanation = '{} {}is{} \'{}\''.format(feature_name,
                g.EXP_SEP, g.EXP_SEP, class_categ.strip())
        return explanation
    feature, threshold = explanation.rsplit(split_char, 1)
    type_of_text = feature[feature.rfind('_derived_'):]
    if type_of_text:
        expl = fix_text_cols(type_of_text.strip(), feature.strip(), split_char,
                             threshold.strip())
        if expl is not None:
            return expl
    variable_types = all_var_types.loc[all_var_types[
        g.DATA_TYPE] == g.DT_CATEGORICAL][g.VARIABLE_NAME].tolist()
    cat_type = False
    for i in variable_types:
        if str(i) in feature:
            cat_type = True
    if threshold.strip()[-1] == ')':
        threshold = threshold.strip()[:-1]
    if (float(threshold) == 0.5 or "==" in explanation) and cat_type:
        for i in variable_types:
            if str(i) in feature:
                feature_1 = feature.replace(i, '')
                feature_1 = feature_1.replace('_', '', 1)
                class_categ = feature_1
                feature_name = str(i)
        if split_char == ">":
            if g.DI_DEBUG_MODE:
                explanation = feature_name + " is " + class_categ
            else:
                explanation = '{} {}is{} \'{}\''.format(feature_name,
                    g.EXP_SEP, g.EXP_SEP, class_categ.strip())
        else:
            if g.DI_DEBUG_MODE:
                explanation = feature_name + " is not " + class_categ
            else:
                explanation = '{} {}is not{} \'{}\''.format(feature_name,
                    g.EXP_SEP, g.EXP_SEP, class_categ.strip())
        return explanation

    ft_name = feature[:feature.rfind("_")]
    datetime_types = all_var_types.loc[all_var_types[
        g.DATA_TYPE] == g.DT_DATETIME][g.VARIABLE_NAME].tolist()
    if feature.strip().endswith('_secs') and float(
            threshold) <= 86400 and ft_name in datetime_types:
        threshold = str(datetime.timedelta(seconds=int(float(threshold))))
        feature = ft_name + '_time'
    else:
        threshold = str(round(float(threshold), 2))

    if split_char == "<=":
        explanation = feature + " is less than equal to {} ".format(threshold)
    else:
        explanation = feature + " is greater than {} ".format(threshold)
    return re.sub('\s+', ' ', explanation)


def filter_duplicate_insights(tree_idx,
                              insight_list,
                              score_list,
                              classes=None):
    classes_list_filtered = list()
    insight_list_filtered = list()
    score_list_filtered = list()
    insight_dict = dict()
    duplicates = []
    for i, insight in enumerate(insight_list):
        if str(insight) not in insight_dict:
            insight_list_filtered.append(insight)
            if classes:
                classes_list_filtered.append(classes[i])
            score_list_filtered.append(score_list[i])
            insight_dict[str(insight)] = True
        else:
            duplicates.append(i)  # only for debugging
    return duplicates, insight_list_filtered, score_list_filtered,\
        classes_list_filtered


def compute_a(b, q):
    sqrt_pi = 1.772453851
    a = np.rint((np.log(1 - q) * 0.88623) / (-(b * sqrt_pi)))
    return a


def compute_a_b(node_counts):
    sorted_counts = node_counts
    # Impute on gap = 1 to compute a and b values
    insert_from_num = node_counts[np.where(np.diff(node_counts) >= 2)]
    insert_to_num = node_counts[np.where(np.diff(node_counts) >= 2)[0] + 1]
    for i, j in zip(insert_from_num, insert_to_num):
        node_counts = np.concatenate(
            (node_counts, np.asarray(range(i + 1, j, 1))))
    node_counts = np.sort(node_counts)

    try:
        b = float(sorted_counts.shape[0]) / float(node_counts.shape[0])
    except ZeroDivisionError as ze:
        b = float(sorted_counts.shape[0]) / 1

    a1 = compute_a(b, 0.995)
    a2 = compute_a(b, 0.999995)
    return a1, a2


def bridge_scheme_imputation(node_counts, a1, a2):
    sorted_counts = node_counts
    # Do not impute if diff is less than a1
    # Impute single number if diff is more than a1 but less than a2
    between_a1_a2_1 = sorted_counts[np.where(
        np.logical_and((np.diff(sorted_counts) - 1) > a1,
                       (np.diff(sorted_counts) - 1) <= a2))]
    between_a1_a2_2 = sorted_counts[np.where(
        np.logical_and((np.diff(sorted_counts) - 1) > a1,
                       (np.diff(sorted_counts) - 1) <= a2))[0] + 1]
    for i, j in zip(between_a1_a2_1, between_a1_a2_2):
        node_counts = np.concatenate(
            (node_counts, np.asarray([i + (j - i - 1) / 2])))
    # If number of missing values > a2
    more_than_a2_1 = sorted_counts[np.where(np.diff(sorted_counts) > a2)]
    more_than_a2_2 = sorted_counts[np.where(np.diff(sorted_counts) > a2)[0] +
                                   1]
    for i, j in zip(more_than_a2_1, more_than_a2_2):
        num_of_values = np.ceil(float(j - i - 1) / a2)
        gap = int((j - i - 1) / num_of_values)
        node_counts = np.concatenate(
            (node_counts, np.asarray(range(i + int(gap), j, int(gap)))))
    node_counts = np.sort(node_counts)
    return node_counts


def inflate_coverage(actual_cov, imputed_cov, mode=None):
    if (mode == "DI" and not g.AUGI_SCORE_OVERFITTING) or (
        mode == "LE" and not g.LE_SCORE_OVERFITTING):
        gold_standard = np.around(np.arange(0.75, 1.0025, 0.0025), decimals=5)
        percentiles = np.around(np.arange(0.05, 1.0095, 0.0095), decimals=5)
    else:
        gold_standard = np.around(np.arange(0.3, 1.007, 0.007), decimals=5)
        percentiles = np.around(np.arange(0, 1.01, 0.01), decimals=2)
    imputed_cov_percentiles = np.around(np.quantile(imputed_cov, percentiles),
                                        decimals=6)
    Tree_model = DecisionTreeRegressor(criterion="squared_error")
    dtc = Tree_model.fit(
        np.array(imputed_cov_percentiles).reshape(-1, 1), gold_standard)
    inflated_cov = dtc.predict(np.array(actual_cov).reshape(-1, 1))
    return inflated_cov, dtc


def compute_node_scores(tot_count, accuracy, mode=None, pruned_nodes=None,
                        dtree_inflate=None):
    if dtree_inflate:
        inflated_coverage = dtree_inflate.predict(np.array(tot_count).reshape(-1, 1))
    else:
        root_node_count = tot_count[0]
        actual_cov = tot_count / float(root_node_count)
        if not g.AUGI_SCORE_OVERFITTING and pruned_nodes is not None:
            tot_count = np.delete(tot_count, pruned_nodes)
        # step-1 Removing root node from computations
        tot_count = tot_count[1:]
        sorted_tot_count = np.sort(np.rint(tot_count))
        normalized_data = 0
        # Normalize distribution if number of nodes in tree are grater than 1000
        if sorted_tot_count[-1] > 1000:
            normalized_data = 1
            num_of_zeros = np.max(tot_count) / 1000.0
            num_to_divide = 10**len(str(int(num_of_zeros)))
            tot_count_float = tot_count / float(num_to_divide)
            tot_count = tot_count_float.astype(int)
        sorted_counts = np.sort(np.rint(tot_count)).astype(int)
        outlier_indices = find_outliers(
            np.array(sorted_counts).reshape(-1, 1))
        outlier_counts = sorted_counts[outlier_indices]
        if len(outlier_indices) != 0:
            sorted_counts = sorted_counts[:min(outlier_indices)]
        # get a1, a2
        a1, a2 = compute_a_b(sorted_counts)
        # Impute with bridge scheme
        imputed_cov_abs = bridge_scheme_imputation(sorted_counts, a1, a2)
        # compute percentiles after including outliers and inflate the coverage
        imputed_cov_abs = np.concatenate((imputed_cov_abs, outlier_counts))
        if normalized_data == 1:
            set_diff = np.setdiff1d(imputed_cov_abs, sorted_counts)
            imputed_cov_abs = np.concatenate(
                (tot_count_float, set_diff.astype(float))) * num_to_divide
        imputed_cov = np.sort(imputed_cov_abs) / float(root_node_count)
        #np.savetxt('Imputed_coverage.txt', imputed_cov, delimiter=',')
        inflated_coverage, dtree_inflate = inflate_coverage(
        actual_cov, imputed_cov, mode=mode)
    scores = np.vectorize(lambda i: min(i, 0.98))(inflated_coverage * accuracy)
    scores = np.around(scores, decimals=6)
    return inflated_coverage, scores, dtree_inflate


def apply_user_perception(scores):
    # Applying user perception on confidence scores
    if np.max(scores) == 0.0:
        return scores
    max_perception = 1.0 / np.max(scores)
    if g.AUGI_PERCEPTION > max_perception:
        # TODO: Write a warning message to user that the entered
        # perception value is grater than max_perception value allowed.
        scores = scores * max_perception
    else:
        scores = scores * g.AUGI_PERCEPTION
    return scores


def get_classification_score(clf, mode='LE', local_g=None):
    if local_g:
        global g
        g = local_g
    leaves_flag = clf.tree_.children_left == -1
    if g.DI_DEBUG_MODE:
        decision_tree_pkl_filename = 'decision_tree_classifier.pkl'
        decision_tree_model_pkl = open(decision_tree_pkl_filename, 'wb')
        pickle.dump(clf, decision_tree_model_pkl)
        decision_tree_model_pkl.close()
    maj_class = np.argmax(np.squeeze(clf.tree_.value), axis=1)
    maj_count = np.max(np.squeeze(clf.tree_.value), axis=1)
    tot_count = np.sum(np.squeeze(clf.tree_.value), axis=1)
    confidence = maj_count / tot_count
    root_node_count = tot_count[0]
    coverage = tot_count / root_node_count

    if not g.AUGI_SIGMOID_SCORING:
        if mode != "LE":
            inflated_coverage, scores, dtree_inflate = compute_node_scores(
                tot_count, confidence, mode=mode, pruned_nodes=clf.pruned_nodes)
        else:
             inflated_coverage, scores, dtree_inflate = compute_node_scores(
                tot_count, confidence, mode=mode)
        sig_th_tuple = None
    else:
        scores_tuple = scoring_model_sigmoid(
            mode, confidence, coverage)
        scores, sig_th_tuple, inflated_coverage, s_accuracy = scores_tuple
        dtree_inflate = None
    # penalizing the scores based on total population
    p_hat = maj_count / root_node_count
    scores_before = np.vectorize(lambda i: min(i, 0.98))(
        inflated_coverage * confidence)
    penalized_scores, b, penalty, factor = penalizing_scores(
        p_hat, tot_count, scores, mode)
    penalized_scores = apply_user_perception(penalized_scores)
    if g.DI_DEBUG_MODE:
        df = pd.DataFrame(zip(leaves_flag, maj_class, confidence, coverage,
                              inflated_coverage, scores_before, maj_count,
                              tot_count, penalized_scores, b, p_hat, penalty),
                          columns=[
                              'Leaves_Flag', 'Maj_Class', 'Accuracy',
                              'Coverage', 'Inflated_Coverage', 'Score_Before',
                              'Maj_Count', 'Tot_Count', 'Penalized_Scores',
                              'B_value', 'P_Hat', 'B/P_Hat'
                          ])
        df.to_csv('scores_df.csv')
        utility.dbglog((leaves_flag, 'Leaves'))
        utility.dbglog((maj_class, 'Majority class per node'))
        utility.dbglog((maj_count, 'Majority count per node'))
        utility.dbglog((tot_count, 'Total number of nodes per node'))
        utility.dbglog((confidence, 'Confidence per node'))
        utility.dbglog((coverage, 'Coverage for each Node'))
        utility.dbglog((scores_before, 'Original scores for each node'))
        utility.dbglog((penalized_scores, 'Penalized scores for each node'))
        # utility.dbglog(("Score sigmoids", sig_th_tuple))
    return penalized_scores, maj_class, maj_count, tot_count, confidence,\
        coverage, sig_th_tuple, p_hat, dtree_inflate, inflated_coverage,\
        scores_before, b, penalty, factor


def build_insight_rule_regression(rule, X, y, scores, score_idx):
    rule_score = rule[0]
    # rule_condition_scores = [t[0] for t in rule[1]]
    rule_conditions = [t[1] for t in rule[1]]
    # rule_filters = [t[2] for t in rule[1]]
    '''
        rule_score (0.97, 46, 0.95, 0.4, 9)
        rule_condition_scores [[(0.97, 74, 0.94, 0.64, 1)],
        [(0.97, 46, 0.95, 0.4, 9)],
        [(0.97, 32, 0.96, 0.28, 13)]]
        rule_conditions ['Evening walk is NO',
        'Work stress level is not LOW',
        'Hours of sleep at night  is less than equal to 7.12500']
    '''
    # initial_accuracy, initial_strength = rule_score[2], rule_score[3]
    # newrules = []
    # candidates = []
    # spin_off_candidates = []
    # Here np.unique is being used because sklearn generates predicted_class from y using np.unique function in it's internals
    # Furthermore, the outcome is lexicographically sorted in sklearn, so np.unique is being used as it does the same.
    # direction_violators = identify_direction_violators(rule_conditions, X, y, np.unique(y)[predicted_class]) # local perspective
    # direction_violators = fast_direction_violators(rule_score, rule_condition_scores)
    # print 'DIRECTION VIOLATORS', direction_violators if g.DI_DEBUG_MODE else "",
    direction_violators = []
    rule_conditions_with_score = [
        ('**' if i in direction_violators else '--', ) + t
        for i, t in enumerate(rule[1])
    ]
    # rule_conditions_with_score = [t for i, t in enumerate(rule[1])]
    # print 'RULE CONDITIONS', rule[1], rule_conditions_with_score if g.DI_DEBUG_MODE else "",
    # rule_list_i = str(rule_score) + '\n' + ",\n".join(rule_conditions_with_score).strip()
    # rule_list_i = rule_list_i.replace(" , ", ", ")
    rule_list_i = [str(rule_score)] + rule_conditions_with_score

    # TODO: comment the following line if optimization needs to be done
    return rule_conditions if not g.DI_DEBUG_MODE else rule_list_i


def get_regression_score(dtc, mode='LE', local_g=None):
    if local_g:
        global g
        g = local_g
    if g.DI_DEBUG_MODE:
        decision_tree_pkl_filename = 'decision_tree_regression.pkl'
        decision_tree_model_pkl = open(decision_tree_pkl_filename, 'wb')
        pickle.dump(dtc, decision_tree_model_pkl)
        decision_tree_model_pkl.close()
    impurity = (dtc.tree_.impurity).round(4)
    leaves_flag = dtc.tree_.children_left == -1
    pred = np.squeeze(dtc.tree_.value)
    rmse = impurity**0.5
    confidence = abs(pred) / (abs(pred) + pow(rmse, g.RMSE_POWER_N))
    confidence[np.isnan(confidence)] = 1
    tot_count = dtc.tree_.n_node_samples.astype(float)
    root_node_count = tot_count[0]
    coverage = tot_count / root_node_count

    if not g.AUGI_SIGMOID_SCORING:
        if mode != "LE":
            inflated_coverage, scores, dtree_inflate = compute_node_scores(
                tot_count, confidence, mode=mode, pruned_nodes=dtc.pruned_nodes)
        else:
            inflated_coverage, scores, dtree_inflate = compute_node_scores(
                tot_count, confidence, mode=mode)
        sig_th_tuple = None
    else:
        sigmoid_tuple = scoring_model_sigmoid(
            mode, confidence, coverage)
        scores, sig_th_tuple, inflated_coverage, s_accuracy = sigmoid_tuple
        dtree_inflate = None
    p_hat = np.multiply(confidence, coverage)
    scores_before = np.vectorize(lambda i: min(i, 0.98))(
        inflated_coverage * confidence)
    penalized_scores, b, penalty, factor = penalizing_scores(
        p_hat, tot_count, scores, mode)
    penalized_scores = apply_user_perception(penalized_scores)
    if g.DI_DEBUG_MODE:
        df = pd.DataFrame(zip(leaves_flag, pred, confidence, coverage,
                              inflated_coverage, scores_before, rmse,
                              tot_count, penalized_scores, b, p_hat,
                              penalty),
                          columns=[
                              'leaves_flag', 'Prediction', 'Accuracy',
                              'Coverage', 'Inflated_Coverage', 'Score_before',
                              'RMSE', 'Tot_count', 'penalized_scores', 'b',
                              'p_hat', 'b/p_hat'
                          ])
        df.to_csv('scores_df.csv')
        utility.dbglog((impurity, 'Impurity per node'))
        utility.dbglog((leaves_flag, 'Leaves'))
        utility.dbglog((pred, 'Predictions'))
        utility.dbglog((rmse, 'RMSE per node'))
        utility.dbglog((confidence, 'Confidence per node'))
        utility.dbglog((tot_count, 'Total number of nodes per node'))
        utility.dbglog((coverage, 'Coverage per node'))
        utility.dbglog((penalized_scores, 'Penalized scores per node'))
    return penalized_scores, rmse, tot_count, confidence, coverage,\
        sig_th_tuple, p_hat, dtree_inflate, inflated_coverage,\
        scores_before, b, penalty, factor


def get_regression_node_score(prevnode, value, dtc, sig_th_tuple,
                              dtree_inflate):
    node_score = []
    impurity = (dtc.tree_.impurity).round(4)
    pred = np.squeeze(dtc.tree_.value)[prevnode]
    rmse = (impurity[prevnode])**0.5
    confidence = abs(pred) / (abs(pred) + pow(rmse, g.RMSE_POWER_N))
    tot_count = dtc.tree_.n_node_samples.astype(float)[prevnode]
    coverage = dtc.tree_.n_node_samples.astype(
        float)[prevnode] / dtc.tree_.n_node_samples[0]
    if not g.AUGI_SIGMOID_SCORING:
        inflated_cov = dtree_inflate.predict(np.array(coverage).reshape(-1, 1))
        scores = np.vectorize(lambda i: min(i, 0.98))(inflated_cov *
                                                      confidence)
    else:
        scores, _, _, _ = scoring_model_sigmoid('DI', confidence, coverage,
                                                sig_th_tuple)
    node_score.append((round(scores, 2), int(tot_count), round(confidence, 2),
                       round(coverage, 2), prevnode))
    return node_score


def fast_direction_violators(rule_score, rule_condition_scores):

    # initialize
    predicted_class = rule_score[1]
    prev_accuracy = 0.0
    violators = []

    # find violators
    for idx, score in enumerate(rule_condition_scores):
        _, maj_class, _, _, accuracy, coverage, _ = score
        if maj_class != predicted_class:
            continue

        if accuracy < prev_accuracy:
            accuracy_pct_drop = (prev_accuracy - accuracy) / prev_accuracy
            if accuracy_pct_drop > abs(g.MAX_ACCEPTABLE_ACCURACY_DROP_LOCAL):
                violators.append(idx - 1)
        prev_accuracy = accuracy

    return violators


def build_insight_rule(rule, X, y, scores, score_idx):
    rule_score = rule[0]
    rule_condition_scores = [t[0] for t in rule[1]]
    rule_conditions = [t[1] for t in rule[1]]
    # rule_filters = [t[2] for t in rule[1]]
    '''
        rule_score (0.91, 0, 15, 15, 1.0, 0.13, 0.91, 0.87, 27)
        rule_condition_scores [(0.4, 2, 46, 115, 0.4, 1.0, 1.0, 0),
        (0.51, 0, 31, 58, 0.53, 0.5, 0.95, 24),
        (0.68, 0, 28, 38, 0.74, 0.33, 0.93, 25),
        (0.86, 0, 28, 30, 0.93, 0.26, 0.92, 26)]
        rule_conditions ['Evening walk is NO',
        'Work stress level is not LOW',
        'Minutes of aerobic exercise  is less than equal to 18.50000',
        'Hours of sleep at night  is less than equal to 7.12500']
    '''
    # predicted_class, initial_accuracy, initial_coverage = rule_score[
    #     1], rule_score[4], rule_score[5]
    # newrules = []
    # candidates = []
    # spin_off_candidates = []
    # Here np.unique is being used because sklearn generates predicted_class from y using np.unique function in it's internals
    # Furthermore, the outcome is lexicographically sorted in sklearn, so np.unique is being used as it does the same.
    # direction_violators = identify_direction_violators(rule_conditions, X, y, np.unique(y)[predicted_class]) # local perspective
    direction_violators = fast_direction_violators(rule_score,
                                                   rule_condition_scores)
    utility.dbglog((
        'DIRECTION VIOLATORS',
        direction_violators if g.DI_DEBUG_MODE else "",
    ))
    rule_conditions_with_score = [
        ('**' if i in direction_violators else '--', ) + t
        for i, t in enumerate(rule[1])
    ]
    # print 'RULE CONDITIONS', rule[1], rule_conditions_with_score if g.DI_DEBUG_MODE else "",
    # rule_list_i = str(rule_score) + '\n' + ",\n".join(rule_conditions_with_score).strip()
    # rule_list_i = rule_list_i.replace(" , ", ", ")
    rule_list_i = [str(rule_score)] + rule_conditions_with_score

    # TODO: comment the following line if optimization needs to be done
    return rule_conditions if not g.DI_DEBUG_MODE else rule_list_i


def build_insights(tree_idx, X, y, clf, all_var_types, scores, maj_class,
                   maj_count, tot_count, confidence, coverage, sig_th_tuple,
                   rule_lime, dtree_inflate, inflated_coverage, scores_before,
                   b, p_hat, penalty, factor):
    if g.DI_DEBUG_MODE:
        debug_list = dict()
    significant_rules = []
    thresholds = {}
    for i in np.unique(maj_class):
        indices = np.where(maj_class == i)[0]
        local_scores = np.sort(scores[indices])
        local_idx = np.argsort(scores[indices])
        thresh = get_knee_threshold(local_scores,
                                    relaxation_angle=0,
                                    min_sample=1,
                                    mode="classification")
        local_indices = local_idx
        indices_for_class_i = indices[local_indices][::-1] - 1
        indices_for_class_i = indices_for_class_i[indices_for_class_i >= 0]
        significant_rules.append(indices_for_class_i)
        thresholds[clf.classes_[i]] = thresh
    rule_list, values_path = get_rules(clf,
                                       X.columns.tolist(),
                                       sig_th_tuple=sig_th_tuple,
                                       is_clf=True,
                                       rule_lime=rule_lime,
                                       dtree_inflate=dtree_inflate)

    insight_list = list()
    score_list = list()
    classes = list()
    if g.DI_DEBUG_MODE:
        debug_list[tree_idx] = debug_list.get(tree_idx, list())
        maj_count_list = list()
        tot_count_list = list()
        confidence_list = list()
        coverage_list = list()
        inflated_coverage_list = list()
        scores_before_list = list()
        b_list = list()
        p_hat_list = list()
        panalty_list = list()
        factor_list = list()
        k_list = list()
    # idx here is the class index (categorical/classification outcome)
    for idx, _ in enumerate(significant_rules):
        if g.ENABLE_FAST_PRUNING:
            # remove pruned nodes from the insight list, score list and classes list
            tmp_sig_arr = list(significant_rules[idx])
            for k in clf.pruned_nodes:
                if k - 1 in significant_rules[idx]:
                    tmp_sig_arr.remove(k - 1)
            significant_rules[idx] = np.array(tmp_sig_arr)
            if len(significant_rules[idx]) == 0:
                continue
        if g.DI_DEBUG_MODE:
            rules = np.array(rule_list)[significant_rules[idx]].tolist()
            tree_info = [(tree_idx + round(scores[k + 1], 2), maj_class[k + 1],
                          int(maj_count[k + 1]), int(tot_count[k + 1]),
                          round(confidence[k + 1], 2), round(coverage[k + 1], 2),
                          round(inflated_coverage[k + 1], 2),
                          round(scores_before[k + 1], 2),
                          round(b[k + 1], 2), round(p_hat[k + 1], 2),
                          round(penalty[k + 1], 2), round(factor[k + 1], 2),
                          k + 1)
                         for k in significant_rules[idx]]
            rule_info = [[
                (node_score[maj_class[significant_rules[idx][i] + 1]],
                 rule_conditions, rule_filters)
                for (node_score, rule_conditions, rule_filters) in rule
            ] for i, rule in enumerate(rules)]
            rules_with_count = zip(tree_info, rule_info)
            debug_list[tree_idx].append(
                [idx, rules, rules_with_count, significant_rules])
            insight_list.extend([
                build_insight_rule(t, X, y, scores,
                                   significant_rules[idx][r_index] + 1)
                for r_index, t in enumerate(rules_with_count)
            ])
            maj_count_list.extend(int(maj_count[
                k + 1]) for k in significant_rules[idx])
            tot_count_list.extend(int(tot_count[
                k + 1]) for k in significant_rules[idx])
            confidence_list.extend(round(confidence[
                k + 1], 2) for k in significant_rules[idx])
            coverage_list.extend(round(coverage[
                k + 1], 2) for k in significant_rules[idx])
            inflated_coverage_list.extend(round(inflated_coverage[
                k + 1], 2) for k in significant_rules[idx])
            scores_before_list.extend(round(scores_before[
                k + 1], 2) for k in significant_rules[idx])
            b_list.extend(round(b[
                k + 1], 2) for k in significant_rules[idx])
            p_hat_list.extend(round(p_hat[
                k + 1], 2) for k in significant_rules[idx])
            panalty_list.extend(round(penalty[
                k + 1], 2) for k in significant_rules[idx])
            factor_list.extend(round(factor[
                k + 1], 2) for k in significant_rules[idx])
            k_list.extend(k + 1 for k in significant_rules[idx])
        else:
            insight_list.extend(
                np.array(rule_list)[significant_rules[idx]].tolist())
        score_list.extend(scores[significant_rules[idx] + 1].round(4).tolist())
        classes.extend(clf.classes_[maj_class[significant_rules[idx] +
                                              1]].tolist())
    if g.DI_DEBUG_MODE:
        df = pd.DataFrame(zip(classes, insight_list, score_list, maj_count_list,
                          tot_count_list, confidence_list,
                          coverage_list, inflated_coverage_list,
                          scores_before_list, b_list, p_hat_list, panalty_list,
                          factor_list, k_list),
                          columns=[
                              'Class', 'Insight', 'Score', 'Maj_Count',
                              'Tot_Count', 'Accuracy', 'Coverage',
                              'Inflated_Coverage', 'Score_Before',
                              'B_value', 'P_Hat', 'B/P_Hat', 'Penalty',
                              'Node Number'
                          ])
        df.to_csv('Insight_list_'+str(tree_idx)+'.csv', index=False)
        pickle.dump((debug_list, insight_list, score_list, classes, X, y),
                    open('debug.pkl', 'wb'))

    # remove duplicate insights, keep the highest score, and then sort by score
    duplicates, insight_list, score_list, classes = filter_duplicate_insights(
        tree_idx, insight_list, score_list, classes)
    sorted_idx = list(np.argsort(score_list)[::-1])
    insight_list = list(map(insight_list.__getitem__, sorted_idx))
    score_list = list(map(score_list.__getitem__, sorted_idx))
    classes = list(map(classes.__getitem__, sorted_idx))
    return duplicates, insight_list, score_list, classes, thresholds


def build_insight_regression(tree_idx, X, y, dtc, scores, rmse, all_var_types,
                             tot_count, confidence, strength, sig_th_tuple,
                             rule_lime, dtree_inflate, inflated_coverage,
                             scores_before, b, p_hat, penalty, factor):
    local_scores = np.sort(scores)
    local_idx = np.argsort(scores)
    thresh = get_knee_threshold(local_scores, relaxation_angle=0, min_sample=1,
                                mode="regression")
    local_indices = local_idx
    local_indices = local_indices[local_indices != 0]
    selected_nodes = local_indices[::-1]
    if g.ENABLE_FAST_PRUNING:
        # remove pruned nodes from the insight list, score list and classes list
        tmp_sig_arr = list(selected_nodes)
        for k in dtc.pruned_nodes:
            if k in selected_nodes:
                tmp_sig_arr.remove(k)
        selected_nodes = np.array(tmp_sig_arr)
    try:
        rule_list, vp = get_rules(dtc,
                                  X.columns.tolist(),
                                  sig_th_tuple=sig_th_tuple,
                                  is_clf=False,
                                  rule_lime=rule_lime,
                                  dtree_inflate=dtree_inflate)
    except Exception as e:
        traceback.print_exc()
        raise e
    outcome_col_name_list_ = list()
    prediction = dtc.tree_.value[selected_nodes].round(3)
    selected_rmse = rmse[selected_nodes].round(3)
    for idx, _ in enumerate(selected_nodes):
        outcome_col_name = str(prediction[idx][0][0]) + '  [+/- ' + str(
            selected_rmse[idx]) + "]"
        outcome_col_name_list_.append(outcome_col_name)
    insight_list_ = np.array(rule_list)[selected_nodes - 1].tolist()
    score_list_ = (scores[selected_nodes].round(4)).tolist()
    if g.DI_DEBUG_MODE:
        rules = np.array(rule_list)[selected_nodes - 1].tolist()
        rules_with_count = zip(
            [(round(tree_idx + scores[k], 2), int(tot_count[k]),
              round(confidence[k], 2), round(strength[k], 2),
              round(inflated_coverage[k], 2), round(scores_before[k], 2),
              round(b[k], 2), round(p_hat[k], 2),
              round(penalty[k], 2), round(factor[k], 2), k)
             for k in selected_nodes], rules)
        insight_list_ = [
            build_insight_rule_regression(t, X, y, scores,
                                          selected_nodes[r_index])
            for r_index, t in enumerate(rules_with_count)
        ]
        tot_count_list_ = (tot_count[selected_nodes].round(4)).tolist()
        confidence_list_ = (confidence[selected_nodes].round(4)).tolist()
        strength_list_ = (strength[selected_nodes].round(4)).tolist()
        inflated_coverage_list_ = (inflated_coverage[selected_nodes].round(4)).tolist()
        scores_before_list_ = (scores_before[selected_nodes].round(4)).tolist()
        b_list_ = (b[selected_nodes].round(4)).tolist()
        p_hat_list_ = (p_hat[selected_nodes].round(4)).tolist()
        penalty_list_ = (penalty[selected_nodes].round(4)).tolist()
        factor_list_ = (factor[selected_nodes].round(4)).tolist()

        df = pd.DataFrame(zip(outcome_col_name_list_, insight_list_, score_list_,
                          tot_count_list_, confidence_list_,
                          strength_list_, inflated_coverage_list_,
                          scores_before_list_, b_list_, p_hat_list_,
                          penalty_list_, factor_list_, selected_nodes),
                          columns=[
                              'Outcome', 'Insight', 'Score', 'Tot_Count',
                              'Accuracy', 'Coverage',
                              'Inflated_Coverage', 'Score_Before',
                              'B_value', 'P_Hat', 'B/P_Hat', 'Penalty',
                              'Node Number'
                          ])
        df.to_csv('Insight_list_'+str(tree_idx)+'.csv', index=False)
    return insight_list_, score_list_, outcome_col_name_list_, thresh


def aggregate_text_columns(expl_list):
    ret_expl = []
    if g.DI_DEBUG_MODE:
        return [x.replace(g.EXP_SEP, '') for x in expl_list]
    text_agg_dict = {}
    feature_dict = {}
    rem_list = []
    for expl in expl_list:
        expl_split = expl.split(g.EXP_SEP)
        if len(expl_split) == 3:
            key = (expl_split[0], expl_split[1])
            if key in text_agg_dict:
                text_agg_dict[key]["val"].append(expl_split[2].strip())
            else:
                text_agg_dict[key] = {
                    "val": [expl_split[2].strip()],
                    'seen': 0
                }
            if key[1] == 'is not':
                if key[0] in feature_dict:
                    feature_dict[key[0]].append(expl)
                else:
                    feature_dict[key[0]] = [expl]
            if key[1] == 'is' and key[0] in feature_dict:
                rem_list.extend(feature_dict[key[0]])

    result_list = []
    for item in expl_list:
        if item not in rem_list:
            result_list.append(item)

    expl_list = result_list
    for expl in expl_list:
        expl_split = expl.split(g.EXP_SEP)
        if len(expl_split) == 3:
            key = (expl_split[0], expl_split[1])
            if text_agg_dict[key]["seen"] == 0:
                tmp_expl = expl_split[0] + expl_split[1] + " [ " + ", ".join(
                    text_agg_dict[key]["val"]) + " ]"
                text_agg_dict[key]["seen"] = 1
                ret_expl.append(tmp_expl)
        else:
            ret_expl.append(expl)
    return ret_expl

def get_sentiment_string_from_val(e_value):
    filler = ""
    if e_value >= 0.85:
        filler += 'very positive'
    elif e_value < 0.85 and e_value >= 0.70:
        filler += 'positive'
    elif e_value < 0.70 and e_value >= 0.501:
        filler += 'slightly positive'
    elif e_value < 0.501 and e_value >= 0.499:
        filler += 'neutral'
    elif e_value < 0.499 and e_value >= 0.35:
        filler += 'slightly negative'
    elif e_value < 0.35 and e_value >= 0.15:
        filler += 'negative'
    else:
        filler += 'very negative'
    return filler


def fix_text_cols(type_of_text, text_column, operator, expln_value):
    if not type_of_text:
        return None
    exp_str = None
    if g.GLOVE_COLS in type_of_text:
        pass
        '''
        if not g.DI_DEBUG_MODE:
            exp_str = ""
        '''
    elif type_of_text == g.SENTIMENT_SCORE:
        filler = 'sentiment is'
        if " in " == operator:
            e_value_l, e_value_h = expln_value.replace("(", "").replace(
                ")", "").split(",")
            lfiller = get_sentiment_string_from_val(float(e_value_l.strip()))
            hfiller = get_sentiment_string_from_val(float(e_value_h.strip()))
            # if lfiller != hfiller:
            #     filler += lfiller + ' to ' + hfiller
            # else:
            #     filler += lfiller
            words_operator = 'in range (' + expln_value.strip().replace(
                "(", "").replace(")", "").strip() + ')'
        else:
            e_value = float(expln_value)
            # filler += get_sentiment_string_from_val(e_value)
            if operator == '>':
                words_operator = 'more than ' + str(round(e_value, 2))
            else:
                words_operator = 'less than ' + str(round(e_value, 2))
        text_column = text_column.split(g.SENTIMENT_SCORE)[0]
        exp_str = '{} {} {}'.format(text_column, filler, words_operator)
    elif g.TOPICS_COLS in type_of_text:
        topic = text_column[text_column.find(g.TOPICS_COLS) +
                            len(g.TOPICS_COLS):].replace('_', ' ')
        text_column = text_column.split(g.TOPICS_COLS)[0]
        if operator == ">":
            exp_str = '{} {}includes{} \'{}\''.format(text_column, g.EXP_SEP,
                                                      g.EXP_SEP, topic)
        else:
            exp_str = '{} {}excludes{} \'{}\''.format(text_column, g.EXP_SEP,
                                                      g.EXP_SEP, topic)
    elif g.CONCEPT_COLS in type_of_text:
        phrase = text_column[text_column.find(g.CONCEPT_COLS[:-1]) + len(
            g.CONCEPT_COLS
        ):].replace(
            '_', ' '
        )  # This assumes that phrase doesn't have an underscore, so that's a todo
        text_column = text_column.split(g.CONCEPT_COLS)[0]
        if operator == ">":
            exp_str = '{} {}includes the phrase{} \'{}\''.format(
                text_column, g.EXP_SEP, g.EXP_SEP, phrase)
        else:
            exp_str = '{} {}excludes the phrase{} \'{}\''.format(
                text_column, g.EXP_SEP, g.EXP_SEP, phrase)
    return exp_str


def aggregate_filter_sort_insights(classes,
                                   insight_list,
                                   score_list,
                                   tree_idxlist,
                                   thresholds,
                                   response_column_name,
                                   all_var_types,
                                   rule_lime,
                                   clf=True):
    try:
        # now sort all the insights by class and score
        df = pd.DataFrame()
        df[response_column_name] = classes
        df["Insights"] = insight_list
        df["Scores"] = score_list
        df[g.AUGI_TREE_INDEX] = tree_idxlist
        if clf:
            df2 = df.sort_values(by=[response_column_name, "Scores"],
                                 ascending=False).reset_index()
        else:
            df["Thresholds"] = thresholds
            df2 = df.sort_values(by=["Scores"], ascending=False).reset_index()
            thresholds = df2["Thresholds"].tolist()

        insight_list = df2["Insights"].tolist()
        classes = df2[response_column_name].tolist()
        score_list = df2["Scores"].tolist()
        tree_idxlist = df2[g.AUGI_TREE_INDEX].tolist()

        feature_tup = {}
        final_dups = []
        un_insight_list = []
        un_classes = []
        un_score_list = []
        threshold_list = []
        un_index_list = []
        for i in range(len(insight_list)):
            inst = insight_list[i]
            if g.DI_DEBUG_MODE:
                inst = [t[2] for t in insight_list[i][1:]]
            if True:
                mod_expln, feature_list, feature_op_dict = refine_explanation(
                    inst)
                feature_list.sort()
                if clf:
                    tup_key = str(
                        (classes[i], feature_list,
                         [feature_op_dict[ft] for ft in feature_list]))
                else:
                    tup_key = str(
                        (feature_list,
                         [feature_op_dict[ft] for ft in feature_list]))
                #tup_key = str((classes[i], feature_list))
                if g.DI_REMOVE_DUPS == True and tup_key in feature_tup:
                    final_dups.append(insight_list[i])
                    continue
                if len(set(feature_list)) > g.AUGI_MAX_INSIGHT_DEPTH:
                    continue
                o_features = []
                for indx, ft in enumerate(feature_list):
                    if ft.strip() in rule_lime['ginfodict']:
                        if rule_lime['ginfodict'][
                                ft.strip()]['type'] == 'categorical':
                            o_features.append(
                                rule_lime['ginfodict'][ft.strip()]['col_name'])
                        else:
                            o_features.append(ft)
                if clf:
                    o_tup_key = str((o_features, classes[i], score_list[i]))
                else:
                    o_tup_key = str((o_features, score_list[i]))
                if o_tup_key in feature_tup:
                    final_dups.append(insight_list[i])
                    continue
                feature_tup[o_tup_key] = True

                feature_tup[tup_key] = True
            if g.DI_DEBUG_MODE:
                mod_expln = inst
            mod_expln = [
                change_explanation(x, all_var_types) for x in mod_expln
            ]
            mod_expln = aggregate_text_columns(mod_expln)
            mod_expln = [x.strip() for x in mod_expln if x]
            if not mod_expln or len(mod_expln) == 0:
                continue
            if g.DI_DEBUG_MODE:
                t_inst = []
                t_inst.append(insight_list[i][0])
                for ti in range(1, len(insight_list[i])):
                    t_tup = insight_list[i][ti][:2] + (
                        mod_expln[ti - 1], ) + insight_list[i][ti][3:]
                    t_inst.append(" ".join([str(tx) for tx in t_tup]))
                mod_expln = t_inst
            t_insight = ",\n".join(mod_expln).strip()
            un_insight_list.append(t_insight)
            un_classes.append(classes[i])
            un_score_list.append(score_list[i])
            un_index_list.append(tree_idxlist[i])
            if not clf:
                threshold_list.append(thresholds[i])
        #utility.dbglog( "Duplicates", final_dups if g.DI_DEBUG_MODE else "",)
    except Exception as e:
        #utility.dbglog( "Exception in aggreagte data inisghts", e)
        traceback.print_exc()
        raise e

    if clf:
        # comment the line below to troubleshoot specific tree
        for c in un_classes:
            if c not in thresholds:
                threshold_list.append(0.6)
            else:
                threshold_list.append(thresholds[c])
        # uncomment the line below to troubleshoot specific tree
        # threshold_list = [0] * len(classes)
    df = pd.DataFrame()
    df[response_column_name] = un_classes
    df["Insights"] = un_insight_list
    df["Scores"] = un_score_list
    df['Thresholds'] = threshold_list
    df[g.AUGI_TREE_INDEX] = un_index_list
    return df


def get_top_explanations(uid, mid, X, y,
                         response_column_name,
                         criterion, rule_lime,
                         var_type, local_g):
    """Given the dataset, extracts top insights from it.

    Args:
        X (pd.DataFrame): Pandas dataframe containing the data
        y (pd.DataFrame): Pandas dataframe containing the outcome column of the dataset
        criterion (str, optional): the criterion of the decision tree. Should be either "gini" or "entropy"
            for classification and should only be equal to mse for regression. Defaults to "mse".

    Returns:
        [pd.DataFrame]: A DataFrame containing three columns: Explanations, Scores and Classes
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame")
    if not isinstance(y, pd.DataFrame) and not isinstance(y, pd.Series):
        raise TypeError("y must be a pandas DataFrame")
    if len(X.columns) < 1:
        raise ValueError(
            "Atleast two features are required for Augmented Intelligence"
        )
    if criterion not in ["gini", "entropy", "mse"]:
        raise ValueError("Criterion must be one of [gini, entropy, mse]")

    sum_uniq = 0
    for col in X.columns:
        sum_uniq += X[col].nunique()
    if sum_uniq == len(X.columns):
        raise ValueError("Atleast two labels are required in any feature for Augmented Intelligence")

    global g
    g = local_g
    if criterion in ["gini", "entropy"]:
        if len(y.unique()) == 1:
            raise ValueError(
                "Atleast two class labels are required for Augmented Intelligence")
        trees = build_tree(X, y, criterion=criterion, type="classification")
        duplicates, insight_list, score_list, classes, tree_idxlist, sig_th_tuple_list, thresholds = [], [], [], [], [], [], dict()
        dtree_inflate_dict = {} 
        class_map = trees[-1].classes_
        for tree_idx, tree in enumerate(trees):
            # # TODO: uncomment the line below to troubleshoot a specific tree
            # if tree_idx != 1:
            #     continue
            try:
                scores, maj_class, maj_count, tot_count, confidence, coverage,\
                    sig_th_tuple, p_hat, dtree_inflate, inflated_coverage,\
                    scores_before, b, penalty, factor = get_classification_score(
                    tree, 'DI')
            except Exception as e:
                utility.dbglog(("Exception in get_classification_score", e))
                traceback.print_exc()
                continue

            try:
                duplicates_, insight_list_, score_list_, classes_, thresholds_ = build_insights(
                    tree_idx, X, y, tree, var_type, scores, maj_class,
                    maj_count, tot_count, confidence, coverage, sig_th_tuple,
                    rule_lime, dtree_inflate, inflated_coverage, scores_before,
                    b, p_hat, penalty, factor)

                if g.DI_DEBUG_MODE:
                    utility.dbglog(("Thresholds for tree %d -"\
                        %tree_idx, thresholds_))
                    utility.dbglog(("Scores for tree %d -"\
                        %tree_idx, score_list_))
                    utility.dbglog(("Maj_class for tree %d -"\
                        %tree_idx, classes_))

                tree_index_ = [tree_idx] * len(insight_list_)
                tree_idxlist += tree_index_
                duplicates += duplicates_
                insight_list += insight_list_
                score_list += score_list_
                sig_th_tuple_list.append(np.asarray(sig_th_tuple))
                dtree_inflate_dict[tree_idx] = dtree_inflate
                if tree_idx != (len(trees) - 1):
                    classes += [class_map[int(x)] for x in classes_]
                else:
                    classes += classes_
                thresholds.update(thresholds_)
            except Exception as e:
                utility.dbglog(("Exception in data insights clf", e))
                traceback.print_exc()
                raise e

        # Global knee detection code. Calculate knee using scores from
        # all the trees of RF and the independent Dtree
        d = dict([(j, i) for i, j in enumerate(sorted(set(class_map)))])
        maj_classes_g = [d[i] for i in classes]
        thresholds_g = dict()
        #utility.dbglog(("Local Thresholds- ", thresholds))
        for i in np.unique(maj_classes_g):
            indices = np.where(maj_classes_g == i)[0]
            local_scores = np.sort(np.array(score_list)[indices])
            thresh = get_knee_threshold(local_scores,
                                        relaxation_angle=0,
                                        min_sample=1,
                                        mode="classification")
            utility.dbglog(("thresh for class %d =" % i, thresh))
            thresholds_g[class_map[int(i)]] = thresh
        #utility.dbglog(("Global Thresholds- ", thresholds_g))
        thresholds = thresholds_g

        try:
            df = aggregate_filter_sort_insights(classes, insight_list,
                                                score_list, tree_idxlist,
                                                thresholds,
                                                response_column_name, var_type,
                                                rule_lime)
        except Exception as e:
            utility.dbglog(("Exception in Aggregate Filter Sort Insights"))
            traceback.print_exc()
            raise e
    else:
        trees = build_tree(X, y, criterion=criterion, type="regression")
        duplicates, outcome_col_name_list, insight_list, score_list, tree_idxlist, sig_th_tuple_list, thresholds = [], [], [], [], [], [], []
        dtree_inflate_dict = {} 
        try:
            for tree_idx, dtc in enumerate(trees):
                try:
                    scores, rmse, tot_count, confidence, strength, sig_th_tuple, p_hat,\
                        dtree_inflate, inflated_coverage, scores_before, b, penalty,\
                        factor = get_regression_score(
                        dtc, 'DI')
                except Exception as e:
                    utility.dbglog(("Exception in get_regression_score", e))
                    traceback.print_exc()
                    continue
                try:
                    insight_list_, score_list_, outcome_col_name_list_, thresh = build_insight_regression(
                        tree_idx, X, y, dtc, scores, rmse, var_type, tot_count,
                        confidence, strength, sig_th_tuple, rule_lime,
                        dtree_inflate, inflated_coverage, scores_before,
                        b, p_hat, penalty, factor)
                except Exception as e:
                    utility.dbglog(
                        ("Exception in build_insight_regression", e))
                    traceback.print_exc()
                    raise e
                duplicates_, insight_list_, score_list_, outcome_col_name_list_ = filter_duplicate_insights(
                    tree_idx, insight_list_, score_list_,
                    outcome_col_name_list_)
                thresholds_ = [thresh for i in insight_list_]
                duplicates += duplicates_
                insight_list += insight_list_
                score_list += score_list_
                outcome_col_name_list += outcome_col_name_list_
                thresholds += thresholds_
                tree_index_ = [tree_idx] * len(insight_list_)
                tree_idxlist += tree_index_
                sig_th_tuple_list.append(np.asarray(sig_th_tuple))
                dtree_inflate_dict[tree_idx] = dtree_inflate
            utility.dbglog((
                "Duplicates",
                duplicates if g.DI_DEBUG_MODE else "",
            ))
        except Exception as e:
            traceback.print_exc()
            raise e
        local_scores = np.sort(score_list)
        thresh = get_knee_threshold(local_scores,
                                    relaxation_angle=0,
                                    min_sample=1,
                                    mode="regression")
        utility.dbglog(('Global Threshold = ', thresh))

        try:
            df = aggregate_filter_sort_insights(outcome_col_name_list,
                                                insight_list, score_list,
                                                tree_idxlist, thresholds,
                                                response_column_name, var_type,
                                                rule_lime, False)
        except Exception as e:
            utility.dbglog(("Exception in Aggregate Filter Sort Insights"))
            traceback.print_exc()
            raise e
    response = {
        g.AUGI_INDEX_DF: df.to_dict(orient='list'),
    }
    response[g.AUGI_TREE_PATH] = config.AUGI_TREES_PATH
    if not g.AUGI_SIGMOID_SCORING:
        inflation_trees = "inflation_trees"
        if not os.path.exists(inflation_trees):
            os.makedirs(inflation_trees)
        inflation_trees_path = inflation_trees + "/" + \
                               uid + "_" + mid + ".pkl"
        pickle.dump(dtree_inflate_dict,
                    open(inflation_trees_path, "wb"))
        response[g.AUGI_INFLATION_TREES_PATH] = inflation_trees_path
        response[g.AUGI_ALPHA_BETA_VAL] = None
    else:
        sig_th_tuple_list = [x.tolist() for x in sig_th_tuple_list]
        response[g.AUGI_ALPHA_BETA_VAL] = sig_th_tuple_list
        response[g.AUGI_INFLATION_TREES_PATH] = None
    if criterion in ["gini", "entropy"]:
        # Store class weight in misc data
        if g.AUGI_CLASS_BALANCE:
            class_wts = compute_class_weight('balanced', np.unique(y), y)
        else:
            class_wts = compute_class_weight(None, np.unique(y), y)
        utility.dbglog((class_wts))
        class_wts = class_wts.tolist()
        wt_dict = dict()
        unique_val = np.unique(y).tolist()
        for x, y in zip(class_wts, unique_val):
            wt_dict[y.upper()] = float(x)
        response[g.AUGI_BALANCE_WEIGHTS] = wt_dict
    return response


def get_validation_scores(uid, mid, tree_idx, cov_list, acc_list, sig_th_tuple,
                          inflation_trees_path, local_g=None):
    global g
    g = local_g
    inflated_coverage, scores = np.array([]), np.array([])
    if sig_th_tuple and len(sig_th_tuple) > 0 and sig_th_tuple[0]:
        for i in range(len(cov_list)):
            scores_tuple = scoring_model_sigmoid(
                'DI', np.array(acc_list[i]), np.array(cov_list[i]),
                sig_th_tuple[0][tree_idx[i]])
            scores_, _, inflated_coverage, _ = scores_tuple
            scores = np.append(scores, scores_)
    else:
        dtree_inflate = pickle.load(open(inflation_trees_path, "rb"))
        for i in range(len(cov_list)):
            inflated_coverage_, scores_, _ = compute_node_scores(
                cov_list[i], acc_list[i], dtree_inflate=dtree_inflate[tree_idx[i]])
            inflated_coverage = np.append(inflated_coverage,
                                          inflated_coverage_[0])
            scores = np.append(scores, scores_[0])
    return scores
