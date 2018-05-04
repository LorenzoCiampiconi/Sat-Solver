import file_handler
import solver
from sat_problem_objects import Formula
def main():

    formula = file_handler.read_files()
    solver.solve(formula)



main()