import file_handler
import solver
from Formula import Formula
def main():

    formula = file_handler.read_files()
    solver.solve(formula)



main()