import random
import numpy as np

sign = [1, -1]


class HeuristicObj:
    def __init__(self, var):
        """
        Object that contains the weight for a specific literal
        :param var:
        """
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
    """
    The pick branching is based on the appearance of not-assigned literal clauses
    The appearance is weighted on the "importance" of the clause,
    if a clause has less not assigned variable is more important
    so more weight will be assigned to the literal
    :param sat_problem: current sat_problem
    :return:
    """
    n_a = sat_problem.n_a

    weighters = []

    for lit in n_a:
        weighters.append(HeuristicObj(lit))
        weighters.append(HeuristicObj(-1 * lit))

    for weighter in weighters:
        for clause in sat_problem.formula.clauses:
            if weighter.lit in clause.c:
                weighter.weight += float(1.0 / (1 + clause.n_ass))

    max = weighters[0]

    for weighter in weighters:
        if weighter.weight > max.weight:
            max = weighter

    return max.lit

