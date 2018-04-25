import numpy as np
import logic_functions as lf


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


def learning_clause(r, r_a, cl):
    """
    Actual function that learn the clause and define the level to backtrack
    :param r: assignment causing the contradiction
    :param r_a: assignments graph
    :param cl: clause causing the contradiction
    :return:
    """
    # get the direct causes of the contradiction
    causes = get_causes(r, r_a)

    # get recursively all the clauses that participate to resolution
    clauses = get_backward_clauses(causes)

    # cutting the graph doing backward resolution
    learnt_clause = cut_graph_with_resolution(clauses, cl)

    # get the list of levels involved in the learnt clauses
    levels = get_levels(cl, cl[:], r_a, IS_ROOT)[0]
    levels.sort()

    if len(levels) == 1:
        # for convenience when only one assignment is the cause of the contradiction
        # then we must assign this variable, so the learnt clause goes from the start
        level = 0
    else:
        # level is chosen in the way that an assignment will be forced with the new learnt clause.
        level = levels[len (levels) - 2]

    # return an object which contains the level to backjump and the learnt clause
    return BacktrackPack(level, learnt_clause)


def get_causes(r, r_a):
    """
    this function is in charge to recover the cause of a CONTRADICTED CLAUSE, so a clause which assigned give to empty clause (FALSE)
    :param r: assignments to clause, those are all negative values with variable of the clause
    :param r_a: assignments graph
    """

    cause = []

    # search among the assignments graph
    for root in r_a:
        if any(var == abs(root.var) for var in np.abs(r)):
            # this assignment has caused the contradiction
            cause.append(root)
        else:
            # check if one of the caused assignment has caused the contradiction
            cause = cause + get_causes(r, root.caused_list)

    return cause


def cut_graph_with_resolution(clauses, cl):
    """
    function that cut the graph using resolution
    :param clauses:
    :param cl:
    :return:
    """
    # start resolve
    for clause in clauses:
        cl = lf.resolution(cl, clause)

    return cl


def get_backward_clauses(causes):
    """
    function to get all causes to resolve with
    :param causes:
    :return:
    """
    clauses = []
    rec_clauses = []

    # collect all the clause that caused the wrong assignment, recursively until reaching a root assignment
    for cause in causes:
        clauses.append(cause.clause)
        if cause.causes:
            rec_clauses = get_backward_clauses(cause.causes_list)

    return clauses + rec_clauses


def get_levels(cl, cl_i, r_a, is_root):
    """
    get all the levels of the variables in clause learnt
    :param cl_i:
    :param is_root:
    :param cl:
    :param r_a:
    :return:
    """
    levels = []
    indexes = []
    for root in r_a:
        if any(-1 * val == root.var for val in cl):
            levels.append(root.l)
            index = cl_i.indexof(-1 * root.var)
            # for optimization and correctness remove value of which we already found level of assignment
            # this is useful when an assignment has multiple root cause, so it will be analyzed more than once
            cl_i.remove(index)
            if not is_root:
                indexes.append(cl.indexof(-1 * root.var))
            if cl:
                # optimization in passing cl and getting the return value,
                # remove literals that has been already considered
                # in the learnt clause in upper level
                levels_i, index = get_levels(cl, cl_i, r_a, not IS_ROOT)
                levels = levels + levels_i
                indexes = indexes + index
            else:
                break
        elif cl:
            # passing true as for the root assignment
            levels_i = get_levels(cl, cl_i, r_a, IS_ROOT)[0]
            levels = levels + levels_i

        else:
            break

    if is_root:
        for index in indexes:
            cl.remove(index)

    return levels, indexes
