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
        model = []
        #todo introduce weight

        j = 0
        k = start_index
        #for each clauses compared with the assignment made
        for cl in r[start_index:]:
            if r. count(1) == 0:
                if (assigned):
                    self.go_next_node(formula, k, r)
                elif cl[self.v_a] == 0:
                    assigned = True
                    self.a[self.v_a] = formula[start_index + j][self.v_a]
                    r = np.multiply(formula, self.a)
                    r = self.find_inductions(formula, r)
                    is_model, var = self.go_next_node(formula, k, r)

                    if is_model:
                        model = var
                        break
                    elif self.v_a in var:
                        assigned = True
                        self.a[self.v_a] = - formula[start_index + j][self.v_a]
                        r = np.multiply(formula, self.a)
                        r = self.find_inductions(formula, r)
                        is_model, var = self.go_next_node(formula, k, r)
                        if is_model:
                            model = var
                            break
                        else:
                            return


                else:
                    unchecked.append(j)

            j += 1
            k += 1

        return True

    def find_inductions(self, formula, r):
        roots = []
        indexes_removed = []
        #can  be improved carrying the induction for every passage?

        #create tree to optimize induction
        for i in range(len(formula)):
            added = False
            current_index = ''

            if r[i].count(1) == 0:
                if r[i].count(0) == 0:
                    return #todo specify condition of return
                else:
                    for j in range(len(roots)):
                        if (np.multiply(roots[j].r_cl, r[i])).count(0) == roots[j].r_cl.count(0):
                            root = induction_node(i, formula[i], r[i], '')
                            if not added:
                                added = True
                                current_index = j
                                root.add_son(roots[j])
                                roots[j] = root
                            else:
                                roots[current_index].addson(roots[j])
                                indexes_removed. append(i)
                        elif(np.multiply(roots[j].r_cl, r[i])).count(0) == r[i].count(0):
                            roots[j].addson(induction_node(i, formula[i], r[i], roots[j]))

            if not added:
                roots.append(induction_node(i, formula[i], r[i], ''))
            else:
                for i in indexes_removed:
                    del roots[i]

        for r in roots:
            try:
                r.induct(self.a)
            except Exception as e:
                raise e







    def go_next_node(self, formula, start_index, r):
        try:
            i = r.index(0)
            next_node = sol_node(self.a, i)
            is_model, var = next_node.find_contradiction_or_learn(formula, start_index, r)
            return is_model, var

        except ValueError:
            indexes = [i for i, x in enumerate(r) if x == -1]
            return False, indexes


class induction_node:
    def __init__(self, i, cl, r_cl, f):
        self.i = i
        self.cl = ''
        self.r_cl = ''
        self.father = ''
        self.sons = []

    def add_son(self,son):
        added = False
        indexes_removed = []
        for i in range(len(self.sons)):
            if (np.multiply(self.sons[i].r_cl, son.r_cl)).count(0) == self.sons[i].r_cl.count(0):
                son.add_son(self.sons[i])
                self.sons[i].father = son
                if not added:
                    added = True
                    self.sons[i] = son
                else:
                    indexes_removed.append(i)
            elif (np.multiply(self.sons[i].r_cl, son.r_cl)).count(0) == son.r_cl.count(0):
                son.father = self.sons[i]
                self.sons[i].add_son(son)
                return

        if not added:
            self.sons.append(son)
        else:
            for i in indexes_removed:
                del self.sons[i]

    def induct(self, a):
        self.r_cl = np.multiply(a, self.cl)
        if(self.r_cl.count(1) != 0):
            return
        else:
            if self.r_cl.count(0) == 1:
                i = self.r_cl.index(1)
                a[i] = self.cl[i]
                for son in self.sons:
                    son.induct(a)
            elif self.r_cl.count(0) == 0:
                raise Exception



