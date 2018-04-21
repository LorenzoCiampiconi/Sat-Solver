class assignment_node:
    def __init__(self, var, causes, l):

        #this node assignment
        self.level = l
        self.var = var
        self.causes = causes
        self.causes_list = []
        self.caused_list = []

    def search_caused(self, node, i):
        """
        Function that search if a node has caused an assignment
        :param node: node of assignment in tree for CDCL
        :param i: number of cause that miss to be found
        :return:
        """
        if self.var in node.causes:
            node.causes_list.append(self)
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

        # remove this assignment
        self.causes.caused.remove(self)


def define_assignment(val, # value to be assigned
                      r_a, # tree of assignment for cdcl
                      a, # assignment list
                      n_a, # un-assigned variables, ordered in a precise way
                      causes, # causes of the assignment
                      l # level of the assignment
                      ):
    # add ass_node for CDCL if not fundamental assignment
    if not causes:
        r_a.append(assignment_node(val, [], l))
    else:
        add_to_caused(assignment_node(val, causes, l), r_a)

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

    current_r_a = r_a[-1]

    i = 0
    for root in r_a:

        if root.level == l:
            current_r_a = r_a[l - 1]
            break

        i += 1

    # remove the caused from the tree of assignment
    for caused in current_r_a.caused_list:
        for r_a_i in r_a:
            r_a_i.remove_caused(caused)

    del r_a[-(len(r_a) - i):]

    define_assignment(-1 * var, r_a, a, n_a, [], l)


def add_to_caused(node, # node of assignment to be added
                  r_a, #root assignments
                  ):
    for root in r_a:
        i = len(node.causes)
        i = root.search_caused(node, i)
        if i == 0:
            break

    return