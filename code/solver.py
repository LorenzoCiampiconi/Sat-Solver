import numpy as np
import dp
import watch_list as wl
import logic_functions as lf
import assignments_graph as ag
import heuristic
from sat_problem_objects import Clause
from sat_problem_objects import Formula
from sat_problem_objects import SatProblem
from cdcl import BacktrackPack
import random

IS_MODEL = True
NO_MODEL = []
TOP_LEVEL = 0
FIRST_LEVEL = 1
EMPTY_CLAUSE = []

# creating a global variable to use for clause learning
learnt_clauses = []


def solve(formula: Formula, ran):
    """
    Receive input of the formula, and if to use Random Pick Branching, launch the solving
    :param formula:
    :param ran:
    :return:
    """
    # new sat_problem
    sat_problem = SatProblem(formula, ran=ran)

    # add watch list
    sat_problem.watch_list = wl.generate_watch_list(formula)

    # starting solving
    is_model, model = top_level_assignments(sat_problem)

    if is_model:
        print("A model has been found")
        print(model)
        print("with " + str(sat_problem.calls) + " calls of subroutine")
        correct = check_solution(model, formula.clauses)
        if correct:
            print("Checked Solution!")
    else:
        correct = True
        print("Unsat")
        print("with " + str(sat_problem.calls) + " calls of subroutine")

    return sat_problem.calls, sat_problem.assignments, correct


def top_level_assignments(sp: SatProblem) -> tuple:
    """
    Higher level of assignments, the one caused by |cl| = 1
    :param sp:
    :return:
    """
    # empty assignment
    sp.a = []

    clauses = sp.formula.clauses

    # if an assignment is forced by a clauses s.t |cl| = 1
    if len(clauses[0].c) == 1:

        # which variables is forced and with what value?
        val = clauses[0].get_first_literal()
        ag.define_assignment(val, sp, [], TOP_LEVEL, clauses[0])

        # propagate the assignment
        sat, backtrack = wl.watch_a_literal(val, sp, TOP_LEVEL)

        n_unsat = sp.formula.count_unsat()

        #
        if sat and n_unsat == 0:
            return IS_MODEL, sp.a

        # contradiction after the propagation of TOP LEVEL assignments --> UNSAT
        if not sat:
            return not IS_MODEL, NO_MODEL

    # ask heuristic for next-assignments and go to next level
    next_assignment = heuristic.pick_branching(sp)
    is_model, model, backtrack = dp.in_depth_assignment(next_assignment, sp, FIRST_LEVEL)

    # if backtrack to this level with no contradiction, then SAT
    if is_model:
        return is_model, model

    # check learnt clause
    else:

        # if clause learnt is empty then UNSAT, outside the while loop
        while not is_model and backtrack.level == 0 and backtrack.clause.c != EMPTY_CLAUSE:

            # retract assignments on lower level than TOP level
            ag.retract_lower_level(sp, level=TOP_LEVEL)

            # no need to add to watch list as |cl| = 1
            ag.define_assignment(backtrack.clause.c[0], sp, [], 0, backtrack.clause)
            # propagate
            is_model, backtrack = wl.watch_a_literal(backtrack.clause.c[0], sp, TOP_LEVEL)

            # if no contradiction found
            if is_model:
                # continue to assign
                if sp.n_a:
                    next_assignment = heuristic.pick_branching(sp)
                    is_model, model, backtrack = dp.in_depth_assignment(next_assignment, sp, FIRST_LEVEL)
                # no contradiction, no assignments remained --> SAT
                else:
                    return is_model, sp.a

            if is_model:
                return is_model, model

        return not IS_MODEL, NO_MODEL


def check_solution(model, cls):
    """
    Function that do a simple check on the solution if SAT
    :param model:
    :param cls:
    :return:
    """
    checked = True

    i = 0

    for cl in cls:
        r = lf.assign_to_clause(cl, model)

        if not any(val > 0 for val in r):
            checked = False
        i += 1

    if checked:
        return True
    else:
        return False





