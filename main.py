import file_handler
import solver
from sat_problem_objects import Formula
def main():

    formula = Formula()
    formula = file_handler.read_files(formula)
    solver.solve(formula, False)



main()