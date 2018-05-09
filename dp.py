import copy
import numpy as np
import assignments_graph as ag
import watch_list as wl
import heuristic
from sat_problem_objects import Formula
from sat_problem_objects import SatProblem
from watch_list import Watcher
import solver
from cdcl import BacktrackPack


# define of boolean that represent a learnt clause
LEARNT = True
EMPTY = False


def in_depth_assignment(var: int,
                        sp: SatProblem,
                        l: int
                        ):
    """

    :param sp: the sat problem, containing assignment, watch list and graph of assignments
    :param var: variable to be assigned, this is the current value deducted from the clause that was being analyzed before the call
    :param l:  level of next nodes
    :return:
    """

    # *********NEW BRANCH*********
    is_model, model, backtrack = branch(var, sp, l)

    sp.calls += 1

    # *********IMPLEMENTING CDCL*********

    # if this is the level to backjump
    while not is_model and backtrack.level == l:

        # retracting subsequent assignments
        ag.retract_lower_level(sp, l)

        if backtrack.clause:

            wl.add_clause_to_watch_list(backtrack.clause, sp.watch_list, not wl.GENERATION, sp.a)

            backtrack.clause.watched_and_move(sp.a)

            for lit in backtrack.clause.c:
                not_contradict, backtrack = wl.watch_a_literal(-1 * lit, sp, l)

                if not not_contradict:
                    return not_contradict, '', backtrack

            if sp.formula.count_unsat() == 0 or not sp.n_a:  # sat as there are no more clause to be satisfied
                return True, sp.a, EMPTY

            next_assignment = heuristic.pick_branching(sp)

            is_model, model, backtrack = in_depth_assignment(next_assignment, sp, l + 1)

    return is_model, model, backtrack


def branch(var: int,
           sp: SatProblem,
           l: int,
           ):

    # assign for this branch
    ag.define_assignment(var, sp, EMPTY, l, not ag.IS_CAUSED)  # causes is empty as it's a root assignment

    # induct assignment
    can_be_model, backtrack = wl.watch_a_literal(var, sp, l)

    if can_be_model:
        if sp.formula.count_unsat() == 0 or not sp.n_a:  # sat as there are no more clause to be satisfied
            return True, sp.a, EMPTY
        else:

            next_assignment = heuristic.pick_branching(sp)
            return in_depth_assignment(next_assignment, sp, l + 1)
    else:
        # no model found
        model = ''
        return can_be_model, model, backtrack

