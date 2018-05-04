import copy
import numpy as np
import assignments_graph as ag
import watch_list as wl
from sat_problem_objects import Formula
from watch_list import Watcher
import solver
from cdcl import BacktrackPack


# define of boolean that represent a learnt clause
LEARNT = True
EMPTY = False


def in_depth_assignment(var: int,
                        formula: Formula,
                        watch_list: list,
                        r_a: list,
                        a: list,
                        n_a: list,
                        l: int
                        ):
    """

    :param formula: Formula input to SAT-Solver
    :param var: variable to be assigned, this is the current value deducted from the clause that was being analyzed before the call
    :param watch_list:
    :param r_a: pick_branching assignment, root for trees that generate the assignment graph
    :param a: list of assignment
    :param n_a: not assigned variables
    :param l:  level of next nodes
    :return:
    """
    print ("Assignments= " + str(a))
    print("Level = " + str(l))

    # *********FIRST BRANCH*********
    is_model, model, backtrack = branch(var, a, formula, r_a, n_a, l, watch_list)

    # *********IMPLEMENTING CDCL*********

    # if this is the level to backjump
    while not is_model and backtrack.level == l:

        print("Backtrack got in level: " + str(l))

        # retracting subsequent assignments
        ag.retract_lower_level(r_a, a, n_a, l)

        if backtrack.clause:

            backtrack.clause.watched_and_move()

            is_model, model, backtrack = branch(backtrack.clause.get_first_literal(), a,
                                                formula, r_a, n_a, l + 1, watch_list)

    return is_model, model, backtrack


def branch(var: int,
           a: list,
           formula: Formula,
           r_a: list,
           n_a: list,
           l: int,
           watch_list: list):

    # assign for this branch
    print(var)
    print(n_a)
    ag.define_assignment(var, r_a, a, n_a, EMPTY, l, not ag.IS_CAUSED)  # causes is empty as it's a root assignment

    # induct assignment
    can_be_model, backtrack = wl.watch_a_literal(watch_list, var, a, n_a, r_a, l)

    if can_be_model:
        if formula.count_unsat() == 0:  # sat as there are no more clause to be satisfied
            return True, a, EMPTY
        else:
            return in_depth_assignment(watch_list[0].watched[0].var[0], formula, watch_list, r_a, a, n_a, l + 1)
    else:
        # no model found
        model = ''
        return can_be_model, model, backtrack

