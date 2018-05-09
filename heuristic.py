import random
import numpy as np

sign = [1, -1]


class HeuristicObj:
    def __init__(self, var):
        self.lit = var
        self.weight = 0


def pick_branching(sat_problem):

    if sat_problem.random:
        return pick_random(sat_problem.n_a)

    else:
        return original_pick_branching(sat_problem)


def pick_random(n_a):

    var = random.sample(n_a, 1)[0]

    return random.sample(sign, 1)[0] * var


def original_pick_branching(sat_problem):

    n_a = sat_problem.n_a

    weighters = []

    for lit in n_a:
        weighters.append(HeuristicObj(lit))
        weighters.append(HeuristicObj(-1 * lit))

    for weighter in weighters:
        for clause in sat_problem.formula.clauses:
            if weighter.lit in clause.c:
                weighter.weight += float(1 / (clause.n_ass + 1))

    weighters.sort(key=lambda elem: elem.weight, reverse=True)

    return weighters[0].lit










def choose_assignment_from_backtracking(clause, n_a):

    for c in clause:

        if abs(c) in n_a:
            return c

