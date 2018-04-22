import numpy as np

SOLVABLE = True

# assign values to var of the clause, if in result there's positive values then the clause is SAT
def assign_to_clause(cl, a):

    ab = np.abs(a)

    return [abs(cl_j) if cl_j in a else -1 * abs(cl_j)  for cl_j in cl if abs(cl_j) in ab]

# function in charge to calculate resolution between two clause
def resolution(cl_1, cl_2):

    boolv_1 = np.abs(cl_1)
    boolv_2 = np.abs(cl_2)

    if set(boolv_1).issubset(boolv_2):

        # calculate solution:
        solution = [var for var in cl_2 if var in cl_1 or abs(var) not in boolv_1]

        # exactly one literal has been removed
        if len(solution) == (len(cl_2) - 1):
            solution.sort(key = lambda var : abs(var), reverse = False)
            return SOLVABLE, solution
        else:
            return not SOLVABLE, solution

    elif set(boolv_2).issubset(boolv_1):

        # calculate solution:
        solution = [var for var in cl_1 if var in cl_2 or abs(var) not in boolv_2]

        # exactly one literal has been removed
        if len(solution) == (len(cl_1) - 1):
            solution.sort(key = lambda var : abs(var), reverse = False)
            return SOLVABLE, solution
        else:
            return not SOLVABLE, []

    else:

        solution = [var for var in cl_2 if -1 * var not in cl_1]

        solution = solution + [var for var in cl_1 if -1 * var not in cl_2 and var not in solution]

        if len(solution) == len(cl_1) + len(cl_2) - 2 - len([elem for elem in cl_1 if elem in cl_2]):

            solution.sort(key = lambda var : abs(var), reverse = False)
            return SOLVABLE, solution

        else:
            return not SOLVABLE, []
