IS_CAUSED = True
FOUND = True


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

    def search_caused(self, node, i, seen):
        """
        Function that search if a node has caused an assignment
        :param node: node of assignment in tree for CDCL
        :param i: number of cause that miss to be found
        :return:
        """

        if self.var in node.causes and self.var not in seen:
            # print("add " + str(node.var) + " to " + str(self.var))
            node.causes_list.append(self)
            self.add_caused(node)
            seen.append(self.var)
            i -= 1
            # print("Now for ass: " +  str(self.var) + "is:")

            '''
            for n in self.caused_list:
                # print(n.var)
                
            '''

        for caused in self.caused_list:
            if i == 0:
                break
            i = caused.search_caused(node, i, seen)

        return i

    def add_caused(self, caused):
        self.caused_list.append(caused)


def define_assignment(val,  # value to be assigned
                      sp,  # current Sat Problem
                      causes,  # causes of the assignment
                      level,  # level of the assignment
                      is_caused  # assignment is caused or is heuristic assignment
                      ):

    sp.assignments += 1

    # print("assigning " + str(val) + " at level " + str(level))

    # add ass_node for CDCL if not fundamental assignment
    if not causes:
        sp.r_a.append(AssignmentNode(val, [], level, is_caused))
    else:
        add_to_caused(AssignmentNode(val, causes, level, is_caused), sp.r_a)

    # add val to ass, opt for having all the assignment done outside the tree for the CDCL
    sp.a.append(val)

    # remove from the assignable variable, need this list because it has a specific order
    sp.n_a.remove(abs(val))


def add_to_caused(node,  # node of assignment to be added
                  r_a,  # root assignments
                  ):
    seen = []
    i = len(node.causes)
    for root in r_a:
        i = root.search_caused(node, i, seen)
        if i == 0:
            break
    return


def retract_lower_level(sp, level):

    # print("Retracting")

    temp = []

    for root in sp.r_a:
        if root.level > level:

            caused_original = root.caused_list[:]
            # print("1st for " + str(root.var) + "going to retract caused:")

            '''
            for caused in root.caused_list:
                print(str(caused.var))
            '''

            # print("remove " + str(root.var))
            temp.append(root)
            sp.a.remove(root.var)
            sp.n_a.append(abs(root.var))

            # print("2nd for " + str(root.var) + "going to retract caused:")
            for caused in caused_original:
                # print(str(caused.var))
                retract_caused_assignment(caused, sp)

    for item in temp:
        sp.r_a.remove(item)


def retract_caused_assignment(assignment_node, sp):

    # print("remove " + str(assignment_node.var))

    var = assignment_node.var

    if var in sp.a:
        sp.a.remove(assignment_node.var)
        sp.n_a.append(abs(assignment_node.var))

    caused_list = assignment_node.caused_list[:]

    # print("from " + str(assignment_node.var) + "retract also")
    for caused in caused_list:
        if caused in assignment_node.caused_list:
            retract_caused_assignment(caused, sp)
            # print(caused.var)

    for cause in assignment_node.causes_list:
        if assignment_node in cause.caused_list:
            cause.caused_list.remove(assignment_node)


def get_node_of_assignment_from_caused(assignment_graph, literal, caused):

    for node in caused.causes_list:

        if node.var == literal:
            return FOUND, node

    return False, ''


def get_node_of_assignment(assignment_graph, literal):

    for node in assignment_graph:

        if node.var == literal:
            return FOUND, node

        elif node.caused_list:
            found, node_f = get_node_of_assignment(node.caused_list, literal)
            if found:
                return FOUND, node_f

    return not FOUND, ''


# ******************* DEBUGGING FUNCTION *********************
def print_graph(r_a):
    for root in r_a:
        # print("level: " + str(root.level) + "ass: " + str(root.var))

        # if root.clause:
            # print("caused by clause" + str(root.clause.c))

        print_graph(root.caused_list)