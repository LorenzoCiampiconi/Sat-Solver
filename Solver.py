import numpy as np
class sol_node:
    def __init__(self):

        self.a  = [] #assignments in this node of  DPLL
        self.Tnode = ''
        self.Fnode = ''

    def find_contradiction_or_learn(self, formula):

        r = np.multiply(formula, self.a)

        for cl in r:
            if np.count(r, 1) == 0:
                if np.count_nonzero != 0
                    a 
        