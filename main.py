import file_handler
import solver
import sys
import time
from sat_problem_objects import Formula
def main():

    print("Welcome to this finally working SAT")

    formula = Formula()

    if len(sys.argv) > 1:
        print("Input has been recognized")
        formula = file_handler.read_files(formula, sys.argv[1])
    else:
        print("No input has been recognized, solving default input")
        formula = file_handler.read_files(formula, input=False)

    print("formula has " + str(formula.v) + "variables and " + str(formula.clauses))

    print("Solving...")

    t = time.time()
    solver.solve(formula, False)
    t = time.time() - t

    print("total time: " + str(t) + " seconds")



main()