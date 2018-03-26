import numpy as np


def first_assignment():
    #order with number of variables and hamming distance with common variables considered
    return

def next_round(a, formula, r, unchecked):
    for i in unchecked:
        cl = r[i]
        if 1 not in cl:
            if 0 in cl:
                next_node = sol_node(a, i)
                return next_node.find_contradiction_or_learn(formula, i, r, unchecked)
            else:
                return False, [k for k, x in enumerate(cl) if x == -1]
    return True, a


def solve():
    first_assignment()


class sol_node:
    def __init__(self, a, i):

        self.a = a  # assignments in this node of  DPLL
        self.v_a = i
        self.inducted = []
        self.Tnode = ''
        self.Fnode = ''
    #todo unchecked = range(len(r))
    def find_contradiction_or_learn(self, formula, start_index, r, unchecked):
        assigned = False
        model = []
        #todo introduce weight

        j = 0
        k = start_index
        #for each clauses compared with the assignment made
        for cl in r[start_index:]:
            if cl.count(1) == 0: #assignment does not satisfy this formula
                if 0 in cl:
                    return False,  [i for i, x in enumerate(cl) if x == -1]
                #todo try to implement exception to optimize
                if cl[self.v_a] == 0 and formula[start_index + j][self.v_a] != 0: #we can assign something to self.va
                    assigned = True
                    self.a[self.v_a] = formula[start_index + j][self.v_a]
                    r = np.multiply(formula, self.a)
                    r = self.find_inductions(formula, r)
                    is_model, var = self.go_next_node(formula, k, r, unchecked)

                    if is_model:
                        model = var
                        return True, model
                    elif self.v_a in var:
                        #todo implement clause learning here
                        self.a[self.v_a] = - formula[start_index + j][self.v_a]
                        r = np.multiply(formula, self.a)
                        r = self.find_inductions(formula, r)
                        is_model, var = self.go_next_node(formula, k, r, unchecked)
                        if is_model:
                            model = var
                            break
                        else:
                            return is_model, var
                    else:
                        return is_model, var
            else:
                unchecked.remove(j)

            j += 1
            k += 1

        if len(unchecked) != 0:
            next_round(self.a, formula, r, unchecked)

        return True, self.a

    def find_inductions(self, formula, r):
        roots = []
        indexes_removed = []
        #can  be improved carrying the induction for every passage?

        #create tree to optimize induction
        for i in range(len(formula)):
            added = False
            current_index = ''

            if 1 not in r[i]:
                if 0 not in r[i]:
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
                                indexes_removed.append(i)
                        elif(np.multiply(roots[j].r_cl, r[i])).count(0) == r[i].count(0):
                            roots[j].addson(induction_node(i, formula[i], r[i], roots[j]))

            if not added:
                roots.append(induction_node(i, formula[i], r[i], ''))
            else:
                for i in indexes_removed:
                    del roots[i]

        for ro in roots:
            try:
                ro.induct(self.a)
            except Exception as e:
                raise e

        return np.multiply(formula, self.a)


    def go_next_node(self, formula, start_index, r, unchecked):
        #todo this function can be optimized, maybe deleted
        for rs in r:
            if 0 in rs:
                i = rs.index(0)
                next_node = sol_node(self.a, i)
                return next_node.find_contradiction_or_learn(formula, start_index, r, unchecked)

            else:
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
        if 1 in self.r_cl:
            return
        else:
            if self.r_cl.count(0) == 1:
                i = self.r_cl.index(1)
                a[i] = self.cl[i]
                for son in self.sons:
                    son.induct(a)
            elif 0 not in self.r_cl:
                raise Exception


