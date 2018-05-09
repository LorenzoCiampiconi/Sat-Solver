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

    # new sat_problem
    sat_problem = SatProblem(formula, random=ran)

    # add watch list
    sat_problem.watch_list = wl.generate_watch_list(formula)

    # starting solving
    is_model, model = top_level_assignments(sat_problem)

    if is_model:
        print("A model has been found")
        print(model)
        print("with " +  str(sat_problem.calls) + " calls of subroutine")
        correct = check_solution(model, formula.clauses)
    else:
        correct = True
        print("Unsat")

    print(correct)
    return sat_problem.calls, sat_problem.assignments, correct


def top_level_assignments(sp: SatProblem) -> tuple:

    # empty assignment
    sp.a = []

    clauses = sp.formula.clauses

    # if an assignment is forced
    if len(clauses[0].c) == 1:

        # which variables is forced and with what value?
        val = clauses[0].get_first_literal()
        ag.define_assignment(val, sp, [], TOP_LEVEL, clauses[0])

        # propagate the assignment
        ok, backtrack = wl.watch_a_literal(val, sp, TOP_LEVEL)

        n_unsat = sp.formula.count_unsat()

        if n_unsat == 0:
            return IS_MODEL, sp.a

        if not ok:
            return not IS_MODEL, NO_MODEL

    if not sp.n_a:
        return not IS_MODEL, NO_MODEL

    next_assignment = heuristic.pick_branching(sp)
    is_model, model, backtrack = dp.in_depth_assignment(next_assignment, sp, FIRST_LEVEL)

    if is_model:
        return is_model, model

    else:

        while not is_model and backtrack.level == 0 and backtrack.clause.c != EMPTY_CLAUSE:


            ag.retract_lower_level(sp, level=TOP_LEVEL)

            backtrack.clause.watched_and_move(sp.a)

            ag.define_assignment(backtrack.clause.c[0], sp, [], 0, backtrack.clause)

            is_model, backtrack = wl.watch_a_literal(backtrack.clause.c[0], sp, TOP_LEVEL)

            if is_model:

                if sp.n_a:
                    next_assignment = heuristic.pick_branching(sp)
                    # print("next heuristic assigment = " + str(next_assignment))
                    is_model, model, backtrack = dp.in_depth_assignment(next_assignment, sp, FIRST_LEVEL)

                else:
                    return is_model, sp.a
            if is_model:
                return is_model, model

        return not IS_MODEL, NO_MODEL


def check_solution(model, cls):

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





