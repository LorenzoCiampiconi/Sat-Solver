import numpy as np
import cdcl
import dp
import induction_graph as ig
import assignments_graph as ag
from cdcl import backjump_pack
from induction_graph import induction_node


def solve(formula):
    # variables not yet assigned
    n_a = list(range(1, formula.v + 1))

    # root assignment
    r_a = []

    # checked clause
    checked = []

    # creating a global variable to use for clause learning
    global clauses
    clauses = formula.c

    isModel, model, level = first_assignment(formula.c, n_a,  r_a, checked) # maybe something is useless

    if(isModel):
        print("model found")
        print(model)
    else:
        print("Unsat")


def first_assignment(cl, n_a, r_a, checked):
    # order with number of variables and hamming distance with common variables considered

    # empty assignment
    a = []

    # todo check again this function
    induction_trees = ig.generate_ind_graph(cl)

    # todo try to find a way to use hamming distance to use the less amount of passage to find UNSAT
    cl.sort(key = lambda sublist : len(sublist), reverse = False)

    # order unchecked variables by appearances in unchecked clause
    n_a.sort(key = lambda n_a_i: sum(1 if (n_a_i in np.abs(cl_i)) else 0 for cl_i in cl), reverse = True)

    # the order grants that

    for cl_i in cl:
        # if an assignment is forced
        if len(cl_i) == 1:

            # which variables is forced and with what value?
            val = cl_i[0]

            # if it hasn't been assigned, assign
            if abs(val) not in np.abs(a):
                # define assignment
                ag.define_assignment(val, r_a, a, n_a, [], 0)
                ig.adjust_ind_graph(abs(val), induction_trees)
                ok, l = dp.induct(a, r_a, n_a, cl, 0, induction_trees)

                if not ok:
                    return False, [], []

            elif -1 * val in a:
                # during the assignment of all the "single" clause we have contradiction ---> UNSAT
                return False, [], []

            break # remove loop, the induction function will grant that clause with single variables will assign

        else:
            break

    return dp.in_depth_assignment(induction_trees[0].var[0], cl, induction_trees, r_a, a, n_a, 1)



