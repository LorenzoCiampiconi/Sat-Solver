import numpy as np


class sol_node:
    def __init__(self, a, i):

        self.a = a  # assignments in this node of  DPLL
        self.v_a = i
        self.inducted = []
        self.Tnode = ''
        self.Fnode = ''

    def find_contradiction_or_learn(self, formula, start_index, r):
        assigned = False
        unchecked = []
        model = ''

        j = 0

        #for each clauses compared with the assignment made
        for cl in r[start_index:]:
            if np.count(r, 1) == 0:
                if (assigned):
                    self.go_next_node(formula, r)
                elif cl[self.v_a] == 0:
                    assigned = True
                    self.a[self.v_a] = formula[start_index + j][self.i]
                    r = np.multiply(formula, self.a)
                    r = self.find_inductions(formula, r)
                    is_model, var = self.go_next_node(formula, r)

                    if is_model:
                        model = var
                        break;
                    elif self.i in var:
                        assigned = True
                        self.a[self.v_a] = - formula[start_index + j][self.i]
                        is_model, var = self.go_next_node(formula, r)
                        if is_model:
                            model = var
                            break;
                        else:
                            return


                else:
                    unchecked.append(j)

            j += 1

        return True

    def find_inductions(self, formula, r):
        root = []
        for i in range(len(formula)):
            if r[i].count(1) == 0 and r[i].count(0) == 1:
                for ro in root:
                    if (tuple(sum(t) for t in zip((ro.r_cl, r[i]))):
                        return







    def go_next_node(self, formula, r):
        try:
            i = r.index(0)
            next_node = sol_node(self.a, i)
            is_model, var = next_node.find_contradiction_or_learn(formula, r)
            return is_model, var

        except ValueError:
            indexes = [i for i, x in enumerate(r) if x == -1]
            return False, indexes


class induction_node:
    def __init__(self):
        cl = ''
        r_cl = ''
        self.father = ''
        self.sons = []