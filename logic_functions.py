import numpy as np

# assign values to var of the clause, if in result there's positive values then the clause is SAT
def assign_to_clause(cl, a):

    ab = np.abs(a)

    return [abs(cl_j) if cl_j in a else -1 * abs(cl_j)  for cl_j in cl if abs(cl_j) in ab]