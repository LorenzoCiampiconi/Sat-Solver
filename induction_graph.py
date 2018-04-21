import numpy as np
import logic_functions as lf
import assignments_graph as ag
import cdcl


class induction_node:
    def __init__(self, i_cl, cl):
        """

        :param i_cl: part of the clause with unassigned variables
        :param cl: complete clause
        """
        self.cl = cl
        self.var = i_cl
        self.sons = []
        self.common = []
        self.sat_by_other = False



# *************************INDUCTION GRAPH FUNCTIONS*************************


def generate_ind_graph(cl):
    """

    :param cl:
    :return:
    """
    induction_roots = []

    # generate an induction tree to optimize induction
    for cl_i in cl: # must be careful to grant order
        add_to_induction_tree(induction_node(cl_i, cl_i), induction_roots)

    return induction_roots

def adjust_ind_graph(var, inductions_roots):
    """

    :param var:
    :param inductions_roots:
    """
    temp = []
    added = []

    adjusted = False
    # this first loop is to check if an induction root must disappear as it has been satisfied or it has finished the variables
    for root in inductions_roots:

        removed = False

        if var in np.abs(root.var):

            if var in root.var:
                temp.append(root)
                added = added + root.sons
                removed = True


            root.var = [var_i for var_i in root.var if abs(var_i) != var]
            adjust_ind_graph(var, root.sons)

            temp_1 = []

            for node in root.common:

                if not any(var_i in node.var for var_i in root.var):
                    node.common.remove(root)
                    temp_1.append(node)

            for item in temp_1:
                root.common.remove(item)

            # WRONG AS EMPTY CLAUSE MEANS THAT IS UNSAT IF NO VALID VARIABLE HAS BEEN FOUND TO BE ASSIGNED
            # if not root.var and not removed:
            #    temp.append(root)
            #    added = added + root.sons

            adjusted = True
    for item in temp:

        inductions_roots.remove(item)

    temp = []

    for item in added:

        add_to_induction_tree(item, inductions_roots)


    if adjusted:
        i = 1
        for root in inductions_roots:

            commons = []

            for root_2 in inductions_roots[i:]:

                if set(np.abs(root.var)).issubset(np.abs(root_2.var)):
                    if root not in temp:
                        temp.append(root)
                        add_to_induction_tree(root_2, root.sons)

                        for r in inductions_roots:
                            if root_2 in r.common:
                                r.common.remove(root_2)
                                root_2.common.remove(r)

                elif set(np.abs(root_2.var)).issubset(np.abs(root.var)):
                    if root_2 not in temp:
                        temp.append(root)
                        add_to_induction_tree(root, root_2.sons)

                        for r in inductions_roots:
                            if root in r.common:
                                r.common.remove(root)
                                root.common.remove(r)

                elif any(var_i in root_2.var for var_i in root.var):
                    commons.append(root_2)

                i += 1

            for r in commons:
                r.common.append(root)
                root.common.append(r)

    for t in temp:
        inductions_roots.remove(t)



def induct_through_tree(root, a, r_a, n_a, l):
    """
    Induction for a root of the induction tree
    :param root: current root
    :param a: assignments
    :param r_a: tree for cdcl
    :param n_a: not assigned variables
    :param l: level
    :return:
    """
    if root.sat_by_other:
        re_added = []

        for son in root.sons:
            ok, item, backtrack = induct_through_tree(son, a, r_a, n_a, l)

            if not ok:

                # propagate backtracking
                return False, [], backtrack

            else:
                re_added.append(item)

        return True, re_added, ''


    elif len(root.var) == 1:

        # it has been caused that all the opposite assignment to his variables
        if abs(root.var[0]) in n_a:
            re_added = []

            causes = [-1 * val for val in root.cl if val != root.var[0]]
            ag.define_assignment(root.var[0], r_a, a, n_a, causes, l)

            for common in root.common:
                if not root.var:
                    stop = True
                remove_var_common(common, root.var[0])

            for son in root.sons:

                if len(son.var) != 1:
                    son.var = [var_i for var_i in son.var if abs(var_i) != abs(root.var[0])]

            for son in root.sons:
                ok, items, backtrack = induct_through_tree(son, a, r_a, n_a, l)

                if not ok:

                    # propagate backtracking
                    return False, '', backtrack

                elif items != son:
                    re_added = re_added + items

            return True, re_added, ''

        else:
            # assignment to the clause that has been contradicted
            r = lf.assign_to_clause(root.cl, a)

            # generation of the object that will backtrack until desired level with learnt clause
            backtrack = cdcl.learning_clause(r, r_a)

            print(backtrack.level)

            # start backtracking
            return False, [], backtrack

    elif not root.var:

        # assignment to the clause that has been contradicted
        r = lf.assign_to_clause(root.cl, a)

        # generation of the object that will backtrack until desired level with learnt clause
        backtrack = cdcl.learning_clause(r, r_a)

        print(backtrack.level)

        # start backtracking
        return False, [], backtrack

    return True, root, []




def add_to_induction_tree(node, induction_roots):

    # temporary list for adding to roots
    temp = []

    added = False

    commons = []

    for root in induction_roots:

        if set(np.abs(root.var)).issubset(np.abs(node.var)):
            add_to_induction_tree(node, root.sons)
            added = True
            break

        elif set(np.abs(node.var)).issubset(np.abs(root.var)):
            temp.append(root)
            add_to_induction_tree(root, node.sons)


        elif any(var_i in node.var for var_i in root.var):
            commons.append(root)



    for r_node in temp:
        induction_roots.remove(r_node)

    if not added:
        induction_roots.append(node)

        for root in commons:
            node.common.append(root)
            root.common.append(node)

def remove_var_common(node, var):

    if var in node.var:
        node.sat_by_other = True
    elif not abs(var) in node.var:
        return

    node.var = [var_i for var_i in node.var if abs(var_i) != abs(var)]

    for son in node.sons:
        remove_var_common(son, var)

