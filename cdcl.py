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

    # print("Contradiction found caused by: " + str(clause.c))

    # print("current assignment:" + str(sp.a))

    # cutting the graph doing backward resolution, idea similar a to the one in minisat
    learnt_clause, levels = analyze_conflict(sp.r_a, clause, level)

    #if not learnt_clause:
        # print("UNSAT FOUND")

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

    print("Clause Learnt:" + str(learnt_clause.c))

    print("go back to level:" + str(level))

    # return an object which contains the level to backjump and the learnt clause
    return BacktrackPack(level, learnt_clause)


def analyze_conflict(r_a, clause, level):
    # print("conflict caused by" + str(clause.c))

    seen = []
    c = clause.c

    levels = []

    learnt = []

    for literal in c:

        if literal not in seen:
            seen.append(literal)
            found, node = ag.get_node_of_assignment(r_a, -1 * literal)

            # if not found:
                # print("ERROR with" + str(-1 * literal))
                # ag.print_graph(r_a)

            if node.level >= level:
                resolution_on_analysis(r_a, -1 * literal, seen, level, levels, learnt)

            elif node.level > 0:
                # print("add to learnt " + str(literal))
                learnt.append(literal)
                levels.append(node.level)

    return learnt, levels


def resolution_on_analysis(r_a, literal, seen, level, levels, learnt):

    # print("solve on" + str(literal))

    found, node = ag.get_node_of_assignment(r_a, literal)

    '''
    if not found:
        print("ERROR caused by " + str(literal))

    if node.clause:
        print("with clause " + str(node.clause.c))

    else:
        print("with no clause ")

    if not found:
        print("ERROR")
    
    '''

    if node.clause:
        # resolve on last assigned, by the structure the first on the clause, will be the last assigned
        # in this case are the causes, so clauses it's the
        clause = node.clause.c[1:]

        for c in clause:
            if c not in seen:
                seen.append(c)

                if node.level >= level:
                    # print("solve on " + str(c))

                    resolution_on_analysis(r_a, -1 * c, seen, level, levels, learnt)

                elif node.level > 0:
                    # print("add to learnt " + str(c))
                    learnt.append(c)
                    levels.append(node.level)

    elif -1 * literal not in learnt and 0 < node.level:
            seen.append(-1 * literal)
            learnt.append(-1 * literal)
            levels.append(node.level)
            # print("add to learnt " + str(-1 * literal))

    return learnt




