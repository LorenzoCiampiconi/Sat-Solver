import numpy as np
import dp
import watch_list as wl
import logic_functions as lf
import assignments_graph as ag
from sat_problem_objects import Clause
from sat_problem_objects import Formula
from cdcl import BacktrackPack

IS_MODEL = True
NO_MODEL = []
TOP_LEVEL = 0
FIRST_LEVEL = 1

# creating a global variable to use for clause learning
learnt_clauses = []


def solve(formula: Formula):

    # root assignment
    r_a = []

    # not assigned variable
    n_a = list(range(1, formula.v + 1))

    watch_list = wl.generate_watch_list(formula)

    # starting solving
    is_model, model = top_level_assignments(formula, n_a, r_a, watch_list) # maybe something is useless

    if is_model:
        print("A model has been found")
        print(model)
        check_solution(model, formula.clauses)
    else:
        print("Unsat")


def top_level_assignments(formula: Formula, n_a: list, r_a: list, watch_list: list) -> tuple:

    # empty assignment
    a = []

    clauses = formula.clauses

    # if an assignment is forced
    if len(clauses[0].c) == 1:

        # which variables is forced and with what value?
        val = clauses[0].get_first_literal()
        ag.define_assignment(val, r_a, a, n_a, [], 0, not ag.IS_CAUSED)

        # propagate the assignment
        ok, backtrack = wl.watch_a_literal(watch_list, val, a, n_a, r_a, TOP_LEVEL)

        n_unsat = formula.count_unsat()

        if n_unsat == 0:
            return IS_MODEL, a

        if not ok:
            return not IS_MODEL, NO_MODEL

    is_model, model, backtrack = dp.in_depth_assignment(n_a[0], formula, watch_list, r_a, a, n_a, FIRST_LEVEL)

    if is_model:
        return is_model, model

    else:

        while backtrack.clause:

            ag.retract_lower_level(r_a, a, n_a, level=TOP_LEVEL)

            is_model, model, backtrack = dp.in_depth_assignment(backtrack.clause.c[0], formula, watch_list,
                                                                r_a, a, n_a, FIRST_LEVEL)

        return not IS_MODEL, NO_MODEL


def check_solution(model, cls):

    checked = True

    for cl in cls:
        r = lf.assign_to_clause(cl, model)

        if not any(val > 0 for val in r):
            print("Wrong model: contradiction found in clause: " + str(cl) + ", " + str(r))
            checked = False

    if checked:
        print("Correct model")





