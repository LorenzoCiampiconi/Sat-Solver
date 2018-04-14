import numpy as np
from Formula import Formula

NO_LEVEL_DECIDED = -1

class ass_node:
    def __init__(self, var, causes, l):

        #this node assignment
        self.level = l
        self.var = var
        self.causes = causes
        self.caused_list = []

    def search_caused(self, node, i):
        """

        :param node: node of assignment in tree for CDCL
        :param i: number of cause that miss to be found
        :return:
        """
        if self.var in node.causes:
            self.add_caused(node)
            i -= 1

        for caused in self.caused_list:
            i = caused.search_caused(node, i)

        return i


    def add_caused(self, caused):
        self.caused_list.append(caused)

    def remove_caused(self, caused):
        # if the caused element is on the "surface" (has not been caused by other assignment caused by this)
        if caused in self.caused_list:
            self.caused_list.remove(caused)

        else: # check if the "caused" has been caused by one of the assignment
            for son_caused in self.caused_list:
                son_caused.remove_caused(caused)

    def retract_assignment(self):
        #remove this assignment
        self.causes.caused.remove(self)

class induction_node:
    def __init__(self, i_cl, cl):
        """

        :param i_cl: part of the clause with unassigned variables
        :param cl: complete clause
        """
        self.cl = cl
        self.var = i_cl
        self.sons = []


def solve(formula):
    # variables not yet assigned
    n_a = list(range(1, formula.v + 1))
    # root assignment
    r_a = []

    #checked clause
    checked = []

    isModel, model = first_assignment(formula.c, n_a,  r_a, checked) #maybe something is useless

    if(isModel):
        print("model found")
        print(model)
    else:
        print("Unsat")


def first_assignment(cl, n_a, r_a, checked):
    #order with number of variables and hamming distance with common variables considered

    # empty assignment
    a = []

    induction_trees = generate_ind_trees(cl)

    # todo try to find a way to use hamming distance to use the less amount of passage to find UNSAT
    list(cl).sort(key = lambda cl_i : len(cl_i), reverse = False)
    #order unchecked variables by appearances in unchecked clause
    n_a.sort(key=lambda n_a_i: sum(1 if (n_a_i in np.abs(cl_i)) else 0 for cl_i in cl), reverse = True)

    #the order grants that

    for cl_i in cl:
        # if an assignemnt is forced
        if len(cl_i) == 1:

            # which variables is forced and with what value?
            val = cl_i[0]

            # if it hasn't been assigned, assign
            if abs(val) not in np.abs(a):
                # define assignemnt
                define_assignment(val, r_a, a, n_a, [], 0)
                adjust_ind_trees(abs(val), induction_trees)
                ok = induct(a, r_a, n_a, cl, 0, induction_trees)

                if not ok:
                    return False, []

            elif -1 * val in a:
                # during the assignment of all the "single" clause we have contradiction ---> UNSAT
                return False, [], []

        else:
            break


    in_depth_assignment(induction_trees[0].var[0], cl, induction_trees, r_a, a, n_a, 1)







def in_depth_assignment(var, # variable to be assigned, this is the current value deducted from the clause that was being analized before the call
                        cl, # list of clauses
                        induction_trees,
                        r_a,  # tree of assignment for CDCL
                        a, # list of assignment
                        n_a, # not assigned variables
                        l #level of next nodes
                        ):

    # order unchecked variables by appearances in unchecked clause
    # n_a.sort(key=lambda n_a_i: sum(1 if (n_a_i in np.abs(cl_i)) else 0 for cl_i in cl), reverse=True)


    # *********FIRST BRANCH*********

    is_model, model, level = branch(var, a, cl, r_a, n_a, l, False)

    #*********SECOND BRANCH*********

    if not is_model and level == l:
        is_model, model, level = branch(var, a, cl, r_a, n_a, l, True)

    elif level != l:
        return is_model, model, level

    return is_model, model,level


def branch(var, a, cl, r_a, n_a, l, second_branch):
    l_a = a[:]  # copy of assignments, local assignment of the first branch
    l_n_a = n_a[:]  # same for not assigned

    # consider only unchecked clauses
    l_cl = [c for c in cl if c not in checked]


    if not second_branch:
        # assign for this branch
        define_assignment(var, r_a, l_a, l_n_a, [], l)  # causes is empty as it's a root assignment
    else:
        invert_assignment(var, r_a, l_a, l_n_a, l)

    # induct assignment
    can_be_model, level = induct(l_a, r_a, l_n_a, l_cl, l_checked, l)

    #
    model = []

    if can_be_model:
        for c in l_cl:
            # recursive call
            can_be_model, model, level = check_clause(c, l_cl, l_a, r_a, l_n_a, l, l_checked)

            if not can_be_model:
                # todo implement cdcl
                break  # go to the other branch

            # this clause has not assigned any variables
            elif model == l_a:
                checked.append(c)

            # inside the recursive call a SAT model has been found, return it
            else:
                break

    else:
        cdcl = True

    return can_be_model, model, level





def define_assignment(val, # value to be assigned
                      r_a, # tree of assignment for cdcl
                      a, # assignment list
                      n_a, # un-assigned variables, ordered in a precise way
                      causes, # causes of the assignment
                      l # level of the assignment
                      ):
    # add ass_node for CDCL if not fundamental assignment
    if not causes:
        r_a.append(ass_node(val, [], l))
    else:
        add_to_caused(ass_node(val, causes, l), r_a)

    # add val to ass, opt for having all the assignment done outside the tree for the CDCL
    a.append(val)

    # remove from the assignable variable, need this list because it has a specific order
    n_a.remove(abs(val))

    # grant order of a
    a.sort(key=lambda a_i: abs(a_i), reverse = False)



def invert_assignment(var, # var of which the assignment must be inverted
                      r_a, # tree of assignment for cdcl
                        a, # assignment list
                      n_a, # un-assigned variables, ordered in a precise way
                      l # level of the assignment
                      ):



    current_r_a = r_a[l-1]

    # remove the caused from the tree of assignment
    for caused in current_r_a.caused_list:
        for r_a_i in r_a:
            r_a_i.remove_caused(caused)

    del r_a[-(len(r_a) - l)]


    define_assignment(-1 * var, r_a, a, n_a, [], l)


# assign values to var of the clause, if in result there's positive values then the clause is SAT
def assign_to_clause(cl, a):

    ab = np.abs(a)

    return [abs(cl_j) if cl_j in a else -1 * abs(cl_j)  for cl_j in cl if abs(cl_j) in ab]


# *****************************INDUCTION TREE***************************** #


def generate_ind_trees(cl):
    """

    :param cl:
    :return:
    """
    induction_roots = []

    # generate an induction tree to optimize induction
    for cl_i in cl: #must be careful to grant order
        add_to_induction_tree(induction_node(cl_i, cl_i), induction_roots)

    return induction_roots

def adjust_ind_trees(var, inductions_roots):
    """

    :param var:
    :param inductions_roots:
    """
    temp = []

    adjusted = False

    for root in inductions_roots:

        if var in np.abs(np.abs(root.var)):
            root.var = [var_i for var_i in root.var if abs(var_i) != var]
            adjust_ind_trees(var, root.sons)
            adjusted = True

    i = 0

    if adjusted:
        i = 0
        for root in inductions_roots:

            for root_2 in inductions_roots[i:]:

                if set(np.abs(root.var)).issubset(np.abs(root_2.var)):
                    if root not in temp:
                        temp.append(root)
                        add_to_induction_tree(root, root_2.sons)

                elif set(np.abs(root_2.var)).issubset(np.abs(root.var)):
                    if root_2 not in temp:
                        temp.append(root)
                        add_to_induction_tree(root, root_2.sons)

    for t in temp:
        inductions_roots.remove(t)


def induct(a,
          r_a,
          n_a,
          cl,
          l,
          induction_roots):
    """

    :param a: assignments
    :param r_a: tree of the assignments
    :param n_a: not assigned variables
    :param cl: clause
    :param l: level
    :return:
    """


    temp = []

    responses = []

    for root in induction_roots:
        ok, re_add = induct_through_tree(root, a, r_a, n_a, l)

        if not ok:
            return False

        elif re_add != root:
            temp.append(root)

            for item in re_add:
                responses. append(item)

    if temp:
        for item in temp:
            induction_roots.remove(item)
        for item in responses:
            add_to_induction_tree(item, induction_roots)

    return True


def induct_through_tree(root, a, r_a, n_a, l):



    if len(root.var) == 1:
        #it has been caused that all the opposite assignment to his variables

        if abs(root.var[0]) in n_a:
            re_added = []

            causes = [-1 * val for val in root.cl if val != root.var[0]]
            define_assignment(root.var[0], r_a, a, n_a, causes, l)

            for son in root.sons:

                if len(son.var) != 1:
                    son.var = [var_i for var_i in son.var if abs(var_i) != root.var[0]]

            for son in root.sons:
                ok, item = induct_through_tree(root.sons, a, r_a, n_a, l)

                if not ok:
                    # todo implement CDCL
                    return False, []

                else:
                    re_added.append(item)

            return True, re_added

        else:
            #todo implement CDCL
            return False, []

    return True, root

def add_to_induction_tree(node, induction_roots):

    # temporary list for adding to roots
    temp = []

    added = False

    for root in induction_roots:

        if set(np.abs(node.var)).issubset(np.abs(root.var)):
            temp.append(root)
            add_to_induction_tree(root, node.sons)

        elif set(np.abs(root.var)).issubset(np.abs(node.var)):
            add_to_induction_tree(node, root.sons)
            added = True
            break


    for r_node in temp:
        induction_roots.remove(r_node)

    if not added:
        induction_roots.append(node)


def decide_level(r, r_a, level):
    # todo verificare
    """

    :param r: assignment to clause
    :param r_a: cdcl tree
    :param level: level, NO_LEVEL_DECIDED DEFINED
    :return:
    """
    for root in r_a:
        if any(var in root.caused_list for var in np.abs(r)) and ( level < 0 or root.level < level):
            level = root.level
        else:
            level = decide_level(r, root.caused_list, level)

    return level



# ******************************CDCL EXTENSION FUNCTION****************************** #

def cdcl():
    #todo
    return

def add_to_caused(node, # node of assignment to be added
                  r_a, #root assignments
                  ):
    for root in r_a:
        i = len(node.causes)
        i = root.search_caused(node, i)
        if i == 0:
            break

    return

