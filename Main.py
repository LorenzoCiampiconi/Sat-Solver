import FileHandler
import Solver
from Formula import Formula
def main():

    formula = FileHandler.read_files()
    Solver.solve(formula)



main()