from sklearn.base import is_classifier
import pandas as pd
import numpy as np
import pickle
from collections import Counter
from sklearn.tree._tree import TREE_LEAF
# internals of explainer model
g = None


def is_leaf(inner_tree, index):
    # Check whether node is leaf node
    return (inner_tree.children_left[index] == TREE_LEAF
            and inner_tree.children_right[index] == TREE_LEAF)


def prune_index(inner_tree, decisions, index=0):
    # Start pruning from the bottom - if we start from the top, we might miss
    # nodes that become leaves during pruning.W
    # Do not use this directly - use prune_duplicate_leaves instead.
    if not is_leaf(inner_tree, inner_tree.children_left[index]):
        prune_index(inner_tree, decisions, inner_tree.children_left[index])
    if not is_leaf(inner_tree, inner_tree.children_right[index]):
        prune_index(inner_tree, decisions, inner_tree.children_right[index])

    # Prune children if both children are leaves now and make the same decision
    if (is_leaf(inner_tree, inner_tree.children_left[index])
            and is_leaf(inner_tree, inner_tree.children_right[index]) and
            (decisions[index] == decisions[inner_tree.children_left[index]]) and
            (decisions[index] == decisions[inner_tree.children_right[index]])):
        # turn node into a leaf by "unlinking" its children
        inner_tree.children_left[index] = TREE_LEAF
        inner_tree.children_right[index] = TREE_LEAF
        # print("Pruned {}".format(index))


def prune_duplicate_leaves(dtree):
    # Remove leaves if both parent and children make same decision
    decisions = dtree.tree_.value.argmax(
        axis=2).flatten().tolist()  # Decision for each node
    prune_index(dtree.tree_, decisions)


def equal_bin(N, m):
    sep = (N.size / float(m)) * np.arange(1, m + 1)
    idx = sep.searchsorted(np.arange(N.size))
    return idx[N.argsort().argsort()]


def get_distribution(dtree, combined_near_points, combined_near_points_outcome,
                     debug=False):
    leaves = dtree.apply(combined_near_points)
    paths = dtree.decision_path(combined_near_points)

    # If it's not a classifier, bin the outcome and convert that to a
    # classification problem
    if not is_classifier(dtree):
        # The below function overestimates the number of bins needed.
        # Based on the experimentation, sqrt of it's estimate proved out to be
        # very useful.
        num_edges = np.histogram_bin_edges(combined_near_points_outcome,
                                           bins='auto').shape[0]
        digitized = equal_bin(combined_near_points_outcome,
                              int(np.sqrt(num_edges)))
    distribution = dict()
    nodes_leaves = dict()
    point_index = -1
    for node_id in paths.indices:
        distribution[node_id] = distribution.get(node_id, [])
        if node_id == 0:
            point_index += 1 
            if is_classifier(dtree):
                distribution[node_id] += [combined_near_points_outcome[point_index]]
            else:
                distribution[node_id] += [digitized[point_index]]
            if node_id != leaves[point_index]:
                nodes_leaves[node_id] = nodes_leaves.get(node_id, set())
                nodes_leaves[node_id].add(leaves[point_index])
        else:
            if is_classifier(dtree):
                distribution[node_id] += [combined_near_points_outcome[point_index]]
            else:
                distribution[node_id] += [digitized[point_index]]
            if node_id != leaves[point_index]:
                nodes_leaves[node_id] = nodes_leaves.get(node_id, set())
                nodes_leaves[node_id].add(leaves[point_index])
    return distribution, nodes_leaves


# fast pruning: compute r(t), p(t) for node 'k'
def rt_pt(distribution, k, combined_near_points):
    if isinstance(distribution[k][0], np.ndarray):
        distribution[k] = distribution[k][0]
        counts = Counter(distribution[k])
    else:
        counts = Counter(distribution[k])
    
    r_t = round(1.0 - ((1.0 * max(counts.values())) / sum(counts.values())), 4)
    p_t = round((1.0 * sum(counts.values())) / combined_near_points.shape[0],
                4)
    return r_t, p_t, counts


def RTt_pt(distribution, nodes_leaves, k, combined_near_points):
    R_Tt = 0
    for leaf in nodes_leaves[k]:
        r_l, p_l, counts = rt_pt(distribution, leaf, combined_near_points)
        R_Tt += r_l * p_l
        # print "\t\t\tPrune Iteration", i, k, L, r_l, p_l, counts
    return round(R_Tt, 4)


def get_node_depths(tree):
    """
    Get the node depths of the decision tree

    >>> d = DecisionTreeClassifier()
    >>> d.fit([[1,2,3],[4,5,6],[7,8,9]], [1,2,3])
    >>> get_node_depths(d.tree_)
    array([0, 1, 1, 2, 2])
    """
    def get_node_depths_(current_node, current_depth, L, R, depths):
        depths += [current_depth]
        if L[current_node] != -1 and R[current_node] != -1:
            get_node_depths_(L[current_node], current_depth + 1, L, R, depths)
            get_node_depths_(R[current_node], current_depth + 1, L, R, depths)

    depths = []
    get_node_depths_(0, 0, tree.children_left, tree.children_right, depths)
    return np.array(depths)


# legacy pruning
def prune(dtree, X, y, mode, distribution, nodes_leaves,
          min_alpha_init=float('inf'), debug=False, local_g=None,
          tree_num=0, source="LE"):
    global g
    g = local_g
    if source == "DI":
        min_alpha_threshold = g.AUGI_MIN_ALPHA_THRESHOLD
        fast_pruning_distance = g.AUGI_FAST_PRUNING_DISTANCE
        pruning_coverage_percentage = g.AUGI_MIN_PRUNING_COVERAGE_PERCENTAGE
        pruning_coverage = g.AUGI_MIN_PRUNING_COVERAGE
    else:
        min_alpha_threshold = g.LE_MIN_ALPHA_THRESHOLD
        fast_pruning_distance = g.LE_FAST_PRUNING_DISTANCE
        pruning_coverage_percentage = g.LE_MIN_PRUNING_COVERAGE_PERCENTAGE
        pruning_coverage = g.LE_MIN_PRUNING_COVERAGE
    
    children_left = dtree.tree_.children_left
    children_right = dtree.tree_.children_right
    prune_list = []
    pruned_nodes_final = []
    node_depths = get_node_depths(dtree.tree_)
    for i in range(10):
        pruned_nodes_temp = []
        if debug:
            utility.dbglog(("Inside pruning"))
        prune_order = []
        min_alpha = min_alpha_init
        min_prune = None
        for k in distribution:
            r_t, p_t, counts_t = rt_pt(distribution, k, X)
            R_t = round(r_t * p_t, 4)
            if k in nodes_leaves:
                R_Tt = RTt_pt(distribution, nodes_leaves, k, X)
                g_t = round((1.0 * (R_t - R_Tt)) / (len(nodes_leaves[k]) - 1),
                            3)
                prune_order.append((k, g_t, len(nodes_leaves[k]), R_t, R_Tt,
                                    r_t, p_t, counts_t))
                # print "\t\tPrune Iteration", i, k, R_t, p_t, counts_t, R_Tt
                #     len(nodes_leaves[k]), nodes_leaves[k], g_t, min_alpha,
                #     min_alpha_threshold, min_prune
                # track prune candidate
                if g_t < min_alpha:
                    min_alpha = g_t
                    min_prune = k

        # min alpha breaking condition
        if min_alpha > min_alpha_threshold:
            break
        # terminate pruning iterations
        if not min_prune:
            break
        prune_order.sort(key=lambda x: x[1])
        len_non_terms = len(prune_order)

        prune_order = [t for t in prune_order if t[1] == min_alpha and
            node_depths[t[0]] >= fast_pruning_distance]
        if len(prune_order) == 0:
            break

        len_pruned_terms = len(prune_order)

        for prune_node_k in prune_order:
            for node in pruned_nodes_temp:
                pruned_nodes_final.append(node)
            pruned_nodes_temp = []
            min_prune_k = prune_node_k[0]
            min_alpha_k = prune_node_k[1]
            if min_prune_k not in nodes_leaves:
                # already pruned in previous iteration
                continue
            max_prune_k = max(nodes_leaves[min_prune_k])
            if debug:
                utility.dbglog(("Pruning: {} {} {} {} {} {}".format(
                    tree_num, i, min_prune_k, min_alpha_k, max_prune_k,
                    max_prune_k - min_prune_k + 1)))
            prune_list += [(min_prune_k, min_alpha_k, max_prune_k)]
            for node in range(min_prune_k + 1, max_prune_k + 1):
                if debug:
                    utility.dbglog('deleting nodes {}'.format(node))
                    utility.dbglog((pruned_nodes_temp, pruned_nodes_final))
                pruned_nodes_temp.append(node)
                if node in nodes_leaves:
                    del nodes_leaves[node]
            
            if min_prune_k in nodes_leaves:
                if source == "LE":
                    pruned_nodes_temp.append(min_prune_k)
                pru_nodes = nodes_leaves[min_prune_k]
                del nodes_leaves[min_prune_k]
                for element in pru_nodes:
                    del distribution[element]
                    for key, value in nodes_leaves.items():
                        if element in value:
                            value.remove(element)
                            if min_prune_k not in value:
                                value.add(min_prune_k)
                    
                children_left[min_prune_k] = TREE_LEAF
                children_right[min_prune_k] = TREE_LEAF
            if debug:
                distribution, nodes_leaves = get_distribution(dtree, X, y)
                utility.dbglog(("Pruned nodes distribution", len(X), [
                    (node, len(distribution[node])) for node in distribution
                ]))
                R_Tt = RTt_pt(distribution, nodes_leaves, 0, X)
                sum_5 = sum_10 = sum_15 = 0
                for node_ in distribution:
                    if len(distribution[node_]) < 5:
                        sum_5 += 1
                    if len(distribution[node_]) < 10:
                        sum_10 += 1
                    if len(distribution[node_]) < 15:
                        sum_15 += 1
                utility.dbglog(
                    ("Pruning: {} {} {} {} {} {} {} {} {} {} {} {} {} {}".
                     format(
                         tree_num, i, '***' if min_alpha_k < 0.007
                         and node_depths[min_prune_k] > 3 else '   ',
                         len_non_terms, len_pruned_terms, min_prune_k,
                         min_alpha_k, max_prune_k, max_prune_k - min_prune_k + 1,
                         R_Tt, Counter(distribution[min_prune_k]), sum_5, sum_10,
                         sum_15)))
    # Pruning nodes with less coverage
    if mode == "classification":
        tot_count = np.sum(np.squeeze(dtree.tree_.value), axis=1)
    else:
        tot_count = dtree.tree_.n_node_samples.astype(float)
    prune_nodes = [
        node for node, _ in enumerate(tot_count) if tot_count[node] < max(
            pruning_coverage, tot_count[0] *
            pruning_coverage_percentage)
    ]
    if debug:
        utility.dbglog(
            ("Pruned nodes with less coverage", prune_nodes, len(X),
             [(node, tot_count[node]) for node, _ in enumerate(tot_count)]))
    for node in prune_nodes:
        children_left[node] = TREE_LEAF
        children_right[node] = TREE_LEAF
        pruned_nodes_final.append(node)

    pruned_nodes_final = list(set(pruned_nodes_final))
    return pruned_nodes_final


# fast pruning: prune the tree based on min alpha
def heuristics_prune(dtree, X, y, distribution, nodes_leaves,
                     min_alpha_init=float('inf'), local_g=None):
    global g
    g = local_g
    children_left = dtree.tree_.children_left
    children_right = dtree.tree_.children_right
    min_alpha = 0
    pruned_nodes = []
    number_of_nodes = dtree.tree_.node_count
    node_depths = get_node_depths(dtree.tree_)
    prune_order = []
    while min_alpha < g.AUGI_MIN_ALPHA_THRESHOLD and len(
            pruned_nodes) < g.FAST_PRUNING_THRESHOLD * number_of_nodes:
        min_alpha = min_alpha_init
        min_prune = None
        for k in distribution:
            R_t, p_t, counts = rt_pt(distribution, k, X)
            R_Tt = 0
            if k in nodes_leaves:
                for leaf in nodes_leaves[k]:
                    r_l, p_l, counts = rt_pt(distribution, leaf, X)
                    R_Tt += r_l * p_l
                g_t = (1.0 * (R_t - R_Tt)) / (float(len(nodes_leaves[k]) - 1))
                g_t = g_t / (node_depths[k] + 1)
                prune_order.append((k, g_t))
                # Please don't remove the code below.
                # It's used to debug pruning so is disabled in production
                # print utility.stamp(), "\t\tPrune Iteration", i, k, l, R_t,\
                #     R_Tt, len(nodes_leaves[k]), nodes_leaves[k], g_t,\
                #     min_alpha, g.AUGI_MIN_ALPHA_THRESHOLD, min_prune
                # track prune candidate
                if g_t < min_alpha:
                    min_alpha = g_t
                    min_prune = k

        pruned_nodes = []
        prune_order.sort(key=lambda x: x[1])
        for (node_no, g_t) in prune_order:
            if node_depths[node_no] > g.FAST_PRUNING_DISTANCE:
                if g_t < g.AUGI_MIN_ALPHA_THRESHOLD:
                    pruned_nodes.append(node_no)
            if len(pruned_nodes) > number_of_nodes * g.FAST_PRUNING_THRESHOLD:
                break

        pruned_nodes_final = []
        for node in pruned_nodes:
            if node in nodes_leaves:
                max_prune = max(nodes_leaves[node])
                for lnode in range(node, max_prune + 1):
                    if lnode in nodes_leaves:
                        pruned_nodes_final.append(lnode)
                        utility.dbglog(('deleting nodes {}'.format(node)))
                        del nodes_leaves[lnode]
                        children_left[lnode] = TREE_LEAF
                        children_right[lnode] = TREE_LEAF
        break
    return pruned_nodes_final


# debugging aid
def trace(sample_id, paths, leaves, feature, combined_near_points, threshold,
          columns, cat_cols, scaler):
    node_index = paths.indices[paths.indptr[sample_id]:paths.indptr[sample_id +
                                                                    1]]
    explanation_quality = 0
    previous_nodes = []
    exp_str = ""
    add_factor = scaler.mean_
    mul_factor = scaler.scale_
    for node_id in node_index:
        if leaves[sample_id] == node_id:
            continue
        col_name = columns[feature[node_id]]
        is_cat_col = False
        actual_col = None
        for cat_col in cat_cols:
            if cat_col in col_name:
                is_cat_col = True
                if cat_col in previous_nodes:
                    explanation_quality = explanation_quality - 2
                    actual_col = cat_col
                    break
        if col_name in previous_nodes:
            explanation_quality = explanation_quality - 2
        else:
            explanation_quality = explanation_quality + 1
        if not is_cat_col and col_name not in previous_nodes:
            previous_nodes.append(columns[feature[node_id]])
        else:
            if actual_col is not None and actual_col not in previous_nodes:
                previous_nodes.append(actual_col)

        # print utility.stamp(), 'The Explanation Quality is',\
        #     explanation_quality
        if (combined_near_points[sample_id, feature[node_id]] <=
                threshold[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"
        exp_str += " " + g.EXP_SEP + "%s (=%s) %s %s" % (
            columns[feature[node_id]],
            str(
                round(
                    combined_near_points[sample_id, feature[node_id]] *
                    mul_factor[feature[node_id]] +
                    add_factor[feature[node_id]], 2)), threshold_sign,
            str(
                round(
                    threshold[node_id] * mul_factor[feature[node_id]] +
                    add_factor[feature[node_id]], 2)))
    return exp_str[2:]


# debugging aid


def print_trace(paths, leaves, feature, combined_near_points,
                combined_near_points_outcome, threshold):
    exp_str = ""
    for i, path in enumerate(paths):
        utility.dbglog(('{}, {}, {}'.format(i, "LEAF-" + str(leaves[i]),
                                            combined_near_points_outcome[i])))
        exp_str = exp_str + ' ' + g.EXP_SEP + ' ' + trace(
            i, paths, leaves, feature, combined_near_points, threshold)
    return exp_str[2:]


# debugging aid
def print_tree(dtree, columns, scaler_path, distribution=None, graph_file=None):
    n_nodes = dtree.tree_.node_count
    children_left = dtree.tree_.children_left
    children_right = dtree.tree_.children_right
    feature = dtree.tree_.feature
    threshold = dtree.tree_.threshold
    if scaler_path is None:
        add_factor = 1
        mul_factor = 1
    else:
        scaler = pickle.load(open(scaler_path, "rb"))
        mul_factor = scaler.scale_
        add_factor = scaler.mean_
    # The tree structure can be traversed to compute various properties such
    # as the depth of each node and whether or not it is a leaf.
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if children_left[node_id] != children_right[node_id]:
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True

    tree_threshold_backup = dict()
    for i in range(n_nodes):
        # For Luis datasets, explain was failing for 1 data point
        # IndexError: index -2 is out of bounds for axis 0 with size 1
        # -2 is for leaf nodes, hence we need to continue
        if feature[i] == -2:  # -2 values is for leaf node
            continue
        if scaler is not None:
            tree_threshold_backup[i] = dtree.tree_.threshold[i]
            dtree.tree_.threshold[i] = round(
                dtree.tree_.threshold[i] * mul_factor[feature[i]] +
                add_factor[feature[i]], 3)

    # TODO: enable only for extreme-debugging
    # for i in range(n_nodes):
    #     if is_leaves[i]:
    #         utility.dbglog(("%sLEAF-%s %s" % (
    #             node_depth[i] * "    ", i, dict(
    #             Counter(distribution.get(i, []))))))
    #     else:
    #         if children_left[i] > 0 and children_right[i] > 0:
    #             utility.dbglog(("%snode-%s if (
    #                 %s <= %s) LF-node-%s else RT-node-%s. %s %s %s"
    #                   % (node_depth[i] * "    ",
    #                      i,
    #                      columns[feature[i]],
    #                      threshold[i],
    #                      children_left[i],
    #                      children_right[i],
    #                      round(mul_factor[feature[i]], 2),
    #                      round(add_factor[feature[i]], 2),
    #                      dict(Counter(distribution.get(i, [])))
    #                      )))
    if graph_file:
        export_graphviz(dtree, out_file=graph_file,
                        node_ids=True, filled=True,
                        feature_names=columns)

    for i in range(n_nodes):
        if feature[i] == -2:  # -2 values is for leaf node
            continue
        if scaler is not None:
            dtree.tree_.threshold[i] = tree_threshold_backup[i]
            # dtree.tree_.threshold[i] = round(
            #     (dtree.tree_.threshold[i] - add_factor[feature[i]]) /
            #     mul_factor[feature[i]], 3)
