import copy
import numpy as np
import assignments_graph as ag
import induction_graph as ig
from induction_graph import induction_node
from cdcl import backjump_pack


# define of boolean that represent a learnt clause
LEARNT = True


def in_depth_assignment(var, # variable to be assigned, this is the current value deducted from the clause that was being analized before the call
                        cl, # list of clauses
                        induction_trees,
                        r_a,  # tree of assignment for CDCL
                        a, # list of assignment
                        n_a, # not assigned variables
                        l #level of next nodes
                        ):
    print (a)
    print(l)
    # order unchecked variables by appearances in unchecked clause
    induction_trees.sort(key=lambda node: sum(1 if (n_a_i in np.abs(node.var)) else 0 for n_a_i in n_a), reverse = False)


    # *********FIRST BRANCH*********

    l_a = a[:]  # copy of assignments, local assignment of the first branch
    l_n_a = n_a[:]  # same for not assigned

    induction_trees_l = copy.deepcopy(induction_trees)
    is_model, model, backtrack = branch(var, l_a, cl, r_a, l_n_a, l, induction_trees_l, [])

    #*********IMPLEMENTING CDCL*********

    while not is_model:

        if backtrack.level == l:

            # adding learnt clause
            global clauses
            clauses.append(backtrack.clause)

            # define unassigned variables of the learnt clause
            var_lc = [var for var in backtrack.clause if abs(var) in l_n_a]

            # define learnt induction node
            l_node = induction_node(var_lc, backtrack.clause)

            # learning
            ig.add_to_induction_graph(l_node, induction_trees_l, LEARNT)

            # assigningvariables after learning
            is_model, model, backtrack = branch(var_lc[0], l_a, cl, r_a, l_n_a, l, induction_trees_l, [])

        else:
            return is_model, model, backtrack

    print (l)

    return is_model, model, backtrack


def branch(var, a, cl, r_a, n_a, l, induction_trees, levels):


    # assign for this branch
    ag.define_assignment(var, r_a, a, n_a, [], l)  # causes is empty as it's a root assignment
    ig.adjust_ind_graph(abs(var), induction_trees)

    # induct assignment
    can_be_model, backtrack = induct(a, r_a, n_a, cl, l, induction_trees)


    if can_be_model:

        if not induction_trees: # sat as there are no more clause to be satisfied
            return True, a, []
        else:
            return in_depth_assignment(induction_trees[0].var[0], cl, induction_trees, r_a, a, n_a, l + 1)
    else:
        # no model found
        model = ''
        return can_be_model, model, backtrack


# *****************************INDUCTION TREE***************************** #


def induct(a,
          r_a,
          n_a,
          cl,
          l,
          induction_roots):
    """
    Unit propagation function that propagate an assignment finding inductions

    :param a: assignments
    :param r_a: tree of the assignments
    :param n_a: not assigned variables
    :param cl: clause
    :param l: level
    :return:
    """
    # temp field for root induction node that must be removed
    temp = []

    # responses in case a root must be removed, some of the sons of this root
    # that must not be removed will be added again
    responses = []

    for root in induction_roots:
        ok, re_add, backtrack = ig.induct_through_tree(root, a, r_a, n_a, l)

        if not ok:
            return False, backtrack

        elif re_add != root:
            temp.append(root)

            for common in root.common:
                common.common.remove(root)

            for item in re_add:
                responses.append(item)

    if temp:
        for item in temp:
            induction_roots.remove(item)
        for item in responses:
            ig.add_to_induction_graph(item, induction_roots, NOT_LEARNT)

    return True, []
