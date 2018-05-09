import numpy as np
import logic_functions as lf
from sat_problem_objects import Clause, Formula, SatProblem
import watch_list as wl
import assignments_graph as ag


IS_ROOT = True
NO_LEVEL_DECIDED = -1
EMPTY_CLAUSE = []


class BacktrackPack:
    def __init__(self, level, clause):
        """
        This class contains the clause learnt after finding a contradiction and the level of the older assignment
        :param level: level to reach with backtracking
        :param clause: learnt clause
        """
        self.clause = clause
        self.level = level


# ****************************** CDCL FUNCTION ****************************** #


def learning_clause(r: list,
                    clause: Clause,
                    sp: SatProblem,
                    level
                    ):
    """
    Actual function that learn the clause and define the level to backtrack
    :param sp: the sat problem, containing assignment, watch list and graph of assignments
    :param clause: clause causing the contradiction
    :param r: assignment causing the contradiction
    :return:
    """

    # cutting the graph doing backward resolution, idea similar a to the one in minisat
    learnt_clause, levels = analyze_conflict(sp.r_a, clause, level)

    learnt_clause = [[lit] for lit in learnt_clause]
    levels = [[l] for l in levels]

    zipped = [a + b for a, b in zip(learnt_clause, levels)]

    zipped.sort(key=lambda elem: elem[1], reverse=False)

    learnt_clause = [a[0] for a in zipped]
    levels = [a[1] for a in zipped]

    if len(learnt_clause) <= 1:
        # for convenience when only one assignment is the cause of the contradiction
        # then we must assign this variable, so the learnt clause goes from the start
        level = 0
    else:
        # level is chosen in the way that an assignment will be forced with the new learnt clause.
        level = levels[len (levels) - 2]

    learnt_clause = Clause(learnt_clause)
    sp.formula.add_learnt_clause(learnt_clause, sp.a, sp.watch_list)

    # return an object which contains the level to backjump and the learnt clause
    return BacktrackPack(level, learnt_clause)


def analyze_conflict(r_a, clause, level):
    seen = []
    c = clause.c

    levels = []

    learnt = []

    set = [clause]

    for literal in c:

        if literal not in seen:
            seen.append(literal)
            found, node = ag.get_node_of_assignment(r_a, -1 * literal)

            if node.clause:
                set.append(node.clause)

            if node.level >= level and node.clause:
                resolution_on_analysis(r_a, node, seen, level, levels, learnt)

            elif node.level > 0:
                learnt.append(literal)
                levels.append(node.level)

    return learnt, levels


def resolution_on_analysis(r_a, node, seen, level, levels, learnt):
    """
    For each literal of a clause to resolve with (the one contained in node), find the assignment node and
    :param r_a: assignment graph
    :param node: node to solve with
    :param seen: already seen literal
    :param level: level of the current node
    :param levels: levels of literals added
    :param learnt: clause learnt at the moment
    :return:
    """
    clause = node.clause.c[1:]

    for c in clause:
        if c not in seen:
            seen.append(c)
            found, next_node = ag.get_node_of_assignment_from_caused(r_a, -1 * c, node)

            if next_node.clause:

                if next_node.level >= level:
                    resolution_on_analysis(r_a, next_node, seen, level, levels, learnt)

                elif next_node.level > 0:
                    learnt.append(c)
                    levels.append(next_node.level)

            else:
                if -1 * next_node.var not in learnt and node.level > 0:
                    seen.append(-1 * next_node.var)
                    learnt.append(-1 * next_node.var)
                    levels.append(next_node.level)

    return learnt




