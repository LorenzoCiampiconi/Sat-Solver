IS_CAUSED = True


class AssignmentNode:
    def __init__(self, var, causes, l, is_caused):
        """

        :param var: value assigned in this node
        :param causes: value causing these assignment
        :param l:
        """
        # this node assignment
        self.level = l
        self.var = var
        self.causes = causes
        self.clause = []

        if is_caused:
            self.clause = is_caused

        self.causes_list = []
        self.caused_list = []

    def is_root(self):

        if self.causes:
            return True
        else:
            return False

    def search_caused(self, node, i):
        """
        Function that search if a node has caused an assignment
        :param node: node of assignment in tree for CDCL
        :param i: number of cause that miss to be found
        :return:
        """

        if self.var in node.causes:
            print("add" + str(self.var))
            node.causes_list.append(self)
            self.add_caused(node)
            i -= 1

        for caused in self.caused_list:
            if i == 0:
                break
            i = caused.search_caused(node, i)

        return i

    def add_caused(self, caused):
        self.caused_list.append(caused)

    def remove_caused(self, caused):
        # if the caused element is on the "surface" (has not been caused by other assignment caused by this)
        if caused in self.caused_list:
            self.caused_list.remove(caused)

        else: # check if the "caused" has been caused by one of the caused assignment
            for son_caused in self.caused_list:
                son_caused.remove_caused(caused)

    def retract_assignment(self):

        # remove this assignment
        self.causes.caused.remove(self)


def define_assignment(val,  # value to be assigned
                      r_a,  # tree of assignment for cdcl
                      a,  # assignment list
                      n_a,  # un-assigned variables, ordered in a precise way
                      causes,  # causes of the assignment
                      level,  # level of the assignment
                      is_caused  # assignment is caused or is heuristic assignment
                      ):

    # add ass_node for CDCL if not fundamental assignment
    if not causes:
        r_a.append(AssignmentNode(val, [], level, is_caused))
    else:
        add_to_caused(AssignmentNode(val, causes, level, is_caused), r_a)

    # add val to ass, opt for having all the assignment done outside the tree for the CDCL
    a.append(val)

    print(val)

    # remove from the assignable variable, need this list because it has a specific order
    n_a.remove(abs(val))


def add_to_caused(node,  # node of assignment to be added
                  r_a,  # root assignments
                  ):
    print("add to ass: " + str(node.var))
    i = len(node.causes)
    for root in r_a:
        i = root.search_caused(node, i)
        if i == 0:
            break
    return


def retract_lower_level(r_a, a, n_a, level):

    temp = []

    for root in r_a:
        if root.level > level:
            temp.append(root)
            a.remove(root.var)
            n_a.append(abs(root.var))
            n_a.sort()
            for caused in root.caused_list:
                retract_caused_assignment(caused, r_a, a, n_a)

    for item in temp:
        r_a.remove(item)


def retract_caused_assignment(assignment_node, r_a, a, n_a):

    print("remove: " + (str(assignment_node.var)))

    a.remove(assignment_node.var)
    n_a.append(abs(assignment_node.var))
    n_a.sort()

    caused_list = assignment_node.caused_list[:]

    for caused in caused_list:
        retract_caused_assignment(caused, r_a, a, n_a)

    for cause in assignment_node.causes_list:
        cause.caused_list.remove(assignment_node)

# ******************* DEBUGGING FUNCTION *********************
