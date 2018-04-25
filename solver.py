import numpy as np
import dp
import induction_graph as ig
import assignments_graph as ag
from cdcl import BacktrackPack

IS_MODEL = True
NO_MODEL = []

# creating a global variable to use for clause learning
learnt_clauses = []


def solve(formula):
    # variables not yet assigned
    n_a = list(range(1, formula.v + 1))

    # root assignment
    r_a = []

    # starting solving
    is_model, model = first_assignment(formula.c, n_a,  r_a) # maybe something is useless

    if is_model:
        print("model found")
        print(model)
    else:
        print("Unsat")


def first_assignment(cls: list, n_a: list, r_a: list) -> tuple:
    # order with number of variables and hamming distance with common variables considered

    # empty assignment
    a = []

    # todo check again this function
    induction_graph = ig.generate_ind_graph(cls)

    # todo try to find a way to use hamming distance to use the less amount of passage to find UNSAT
    cls.sort(key = lambda sublist : len(sublist), reverse = False)

    # order unchecked variables by appearances in unchecked clause
    n_a.sort(key = lambda n_a_i: sum(1 if (n_a_i in np.abs(cl_t)) else 0 for cl_t in cls), reverse=True)

    # the order grants that

    # if an assignment is forced
    if len(cls[0]) == 1:

        # as the clauses are ordered by length
        cl_i = cls[0]

        # which variables is forced and with what value?
        val = cl_i[0]

        # if it hasn't been assigned, assign
        if abs(val) not in np.abs(a):

            # define assignment
            ag.define_assignment(val, r_a, a, n_a, [], 0)

            # adjust the graph after the assignment,
            ig.adjust_ind_graph(abs(val), induction_graph)

            # propagate the assignment
            ok, l = dp.induct(a, r_a, n_a, cls, 0, induction_graph)

            if not ok:
                return False, NO_MODEL, []

        elif -1 * val in a:
            # during the assignment of all the "single" clause we have contradiction ---> UNSAT
            return False, NO_MODEL, []

    is_model, model, backtrack = dp.in_depth_assignment(induction_graph[0].var[0], cls, induction_graph, r_a, a, n_a, 1)

    if is_model:
        return is_model, model, backtrack

    else:
        if backtrack.clause:
            for clause in learnt_clauses:
                if clause not in cls:
                    cls.append(clause)
                    # define unassigned variables of the learnt clause
                    var_lc = [val for val in backtrack.clause if abs(val) in n_a]
                    # define learnt induction node
                    l_node = ig.InductionNode(var_lc, backtrack.clause)

            if backtrack.clause not in cls:
                cls.append(backtrack.clause)
                # define unassigned variables of the learnt clause
                var_lc = [val for val in backtrack.clause if abs(val) in n_a]
                # define learnt induction node
                l_node = ig.InductionNode(var_lc, backtrack.clause)

                # learning
                ig.add_to_induction_graph(l_node, induction_graph, ig.LEARNT)

        else:
            return not IS_MODEL, NO_MODEL



