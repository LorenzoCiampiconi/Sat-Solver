import numpy as np

SOLVABLE = True


def is_satisfied(clause, a):
    """
    return True if a variable has been satisfied, False otherwise
    :param clause:
    :param a:
    :return:
    """
    ass = assign_to_clause(clause, a)

    return any(ass_i > 0 for ass_i in ass)


def assign_to_clause(clause, a):
    """
    assign values to var of the clause, if in result there's positive values then the clause is SAT
    :param clause:
    :param a:
    :return:
    """
    cl = clause.c

    ab = np.abs(a)

    return [abs(cl_j) if cl_j in a else -1 * abs(cl_j) for cl_j in cl if abs(cl_j) in ab]
