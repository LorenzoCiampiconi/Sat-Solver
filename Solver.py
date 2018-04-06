import numpy as np
from collections import Counter
from Formula import Formula

class ass_node:
    def __init__(self, var, causes, l):

        #this node assignment
        self.level = l
        self.var = var
        self.causes = causes
        self.caused_list = []

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

def solve(formula):

    # empty assignment
    a = []
    # variables not yet assigned
    n_a = list(range(1, formula.v + 1))
    # root assignment
    r_a = []
    # index for unchecked clauses
    u_i = 0

    isModel, model = first_assignment(formula.c, a, n_a, u_i, r_a) #maybe something is useless

    if(isModel):
        print("model found")
        print(model)
    else:
        print("Unsat")


def first_assignment(formula, a, n_a, unchecked, r_a):
    #order with number of variables and hamming distance with common variables considered

    # todo try to find a way to use hamming distance to use the less amount of passage to find UNSAT
    list(formula).sort(key = lambda sublist : len(sublist), reverse = False)
    #order unchecked variables by appearances in unchecked clause
    n_a.sort(key=lambda n_a_i: sum(a_i.count(n_a_i) for a_i in a), reverse = True)
    i = 0
    for cl in formula:
        # if an assignemnt is forced
        if len(cl) == 1:

            # which variables is forced and with value?
            val = cl[0]

            # if it hasn't been assigned, assign
            if abs(val) not in abs(a):
                # define assignemnt
                define_assignment(val, r_a, a, n_a, [], 0)

            elif -1 * val in a:
                # during the assignment of all the "single" clause we have contradiction ---> UNSAT
                return False, [], []

        else:
            #get if cl is sat
            r = assign_to_clause(cl, a)

            #this is the next cl that must be satisfied
            if 1 not in np.sign(r):

                #not all the variables in clauses cl has been assigned
                if len(r) != len(a):

                    #todo improve the code here, find the assignable variable and assign the first in the ordered unassigned var list, THIS SYNTAX IS ORRIBLE
                    assignable = [var for var in n_a if var in abs(cl)]
                    var = cl[list(np.abs(cl)).index(assignable[0])]

                    return in_depth_assignment(var, cl, unchecked,
                                               r_a[:], a[:], n_a[:],  # passing this list by value and not by argument, change must be local to branch
                                               1 #next level
                                               )

                else:
                    #after have assigned all the "single" clause we have contradiction ---> UNSAT
                    return False, []
        # augment index for unchecked clauses
        unchecked += 0




def in_depth_assignment(var, # variable to be assigned, this is the current value deducted from the clause that was being analized before the call
                        cl, # list of clauses
                        unchecked, # unchecked clauses
                        r_a,  # tree of assignment for CDCL
                        a, # list of assignment
                        n_a, # not assigned variables
                        l #level of next nodes
                        ):



    # *********FIRST BRANCH*********

    l_a = a[:]  # copy of assignments, local assignment of the first branch
    l_n_a = n_a[:] # same for not assigned

    #assign for this branch
    define_assignment(var, r_a, l_a, l_n_a, [], l)  # causes is empty as it's a root assignment

    #induct assignment
    induct(l_a, r_a, l_n_a, cl)


    local_u = unchecked

    #try other
    invert = False

    #
    for c in cl[unchecked:]:
        #recursive call
        can_be_model, model = check_clause(cl, a, r_a, n_a, local_u, l)

        if not can_be_model:
            #todo implement cdcl
            l_a = a[:]
            invert = True
            break #go to the other branch

        #this clause has not
        elif model == a:
            local_u += 1

        else:
            return can_be_model, model



    #*********SECOND BRANCH*********

    l_a = a[:]  # copy of assignments, local assignment of the first branch
    l_n_a = n_a[:]  # same for not assigned

    # assign for this branch
    define_assignment(var, r_a, l_a, l_n_a, [], l)  # causes is empty as it's a root assignment

    # induct assignment
    induct(l_a, r_a, l_n_a, cl)

    local_u = unchecked

    if invert:
        invert_assignment(var, r_a, l_a, l_n_a, l)

        for c in cl[unchecked:]:
            # recursive call
            can_be_model, model = check_clause(cl, a, r_a, n_a, local_u, l)

            if not can_be_model:
                #todo implement cdcl
                l_a = a[:]
                return can_be_model, model

                # this clause has not
            elif model == a:
                local_u += 1

            else:
                return can_be_model, model

    else: #all clauses have been checked and have been satisfied, no contradiction found --> return model
        return True, a




def define_assignment(val, # value to be assigned
                      r_a, # tree of assignment for cdcl
                      a, # assignment list
                      n_a, # un-assigned variables, ordered in a precise way
                      causes, # causes of the assignment
                      l # level of the assignment
                      ):
    # add ass_node for CDCL
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

def induct(l_a, r_a, l_n_a, cl):
    return


def invert_assignment(var, # var of which the assignment must be inverted
                      r_a, # tree of assignment for cdcl
                        a, # assignment list
                      n_a, # un-assigned variables, ordered in a precise way
                      l # causes of the assignment
                      ):

    last_r_a = r_a[-1]

    # remove the caused from the tree of assignment
    for caused in last_r_a.caused_list:
        for r_a_i in r_a:
            r_a_i.remove_caused(caused)


    define_assignment(-1 * var, r_a, a, n_a, [], l)


#assign values to var of the clause
def assign_to_clause(cl, a):

    ab = np.abs(a)

    return [abs(cl_j) if cl_j in a else -1 * abs(cl_j)  for cl_j in cl if abs(cl_j) in ab]

def check_clause(cl, a, r_a, n_a, unchecked, l):
    # get if cl is sat
    r = assign_to_clause(cl, a)

    # this is the next cl that must be satisfied
    if 1 not in np.sign(r):

        # not all the variables in clauses cl has been assigned
        if len(r) != len(a):

            # todo improve the code here, find the assignable variable and assign the first in the ordered unassigned var list, THIS SYNTAX IS ORRIBLE
            assignable = [var for var in n_a if var in abs(cl)]
            var = cl[list(np.abs(cl)).index(assignable[0])]

            return in_depth_assignment(var, cl, unchecked,
                                       r_a[:], a[:], n_a[:],
                                       # passing this list by value and not by argument, change must be local to branch
                                       l + 1  # next level
                                       )

        else:
            # after have assigned all the "single" clause we have contradiction ---> UNSAT
            return False, []
    else:
        return True, a

#******************************CDCL EXTENSION FUNCTION******************************#

def cdcl():
    #todo
    return


def add_to_caused(node, # node of assignment to be added
                  r_a, #root assignments
                  ):
    #todo add to caused
    for a in r_a if: