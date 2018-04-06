import FileHandler
import Solver
from Formula import Formula
def main():

    formula = FileHandler.read_files()
    formula.define_cmatrix()
    Solver.solve(formula)



main()