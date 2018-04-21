NO_LEVEL_DECIDED = -1


class backjump_pack:
    def __init__(self, level, clause):
        """
        This class contains the clause learnt after finding a contradiction and the level of the older assignment
        :param level: level to reach with backtracking
        :param clause: learnt clause
        """
        self.clause = clause
        self.level = level


# ******************************CDCL FUNCTION****************************** #

def learning_clause(r, r_a):

    # get the direct causes of the contradiction
    causes = get_causes(r, r_a)

    # cut the graph and get the root causes
    root_causes = []

    for cause in causes:
        root_causes = root_causes + get_root_cause(cause)

    # get the lower level to backtrack and build the learnt clause
    levels = []
    learnt_clause = []
    for cause in root_causes:
        # save levels
        levels.append(cause.level)
        # learnt clause
        learnt_clause.append(-1 * cause.var) # appending opposite assignment to a clause, so putting in OR all the root assignment flipped that causes the contradiction

    levels.sort()

    if len(levels) == 1:
        # for convenience when only one assignment is the cause of the contradiction then we must assign this variable, so the learnt clause goes from the start
        level = 0
    else:
        #level is chosen in the way that an assignment will be forced with the new learnt clause.
        level = levels[len (levels) - 2]

    # return an object which contains the level to backjump and the learnt clause
    return backjump_pack(level, learnt_clause)


def get_causes(r, r_a):
    """
    this function is in charge to recover the cause of a CONTRADICTED CLAUSE, so a clause which assigned give to empty clause (FALSE)
    :param r: assignments to clause, those are all negative values with variable of the clause
    :param r_a: assignments graph
    """

    cause = []

    # search among the assignments graph
    for root in r_a:
        if any(var == abs(root.var) for var in np.abs(r)):
            # this assignment has caused the contradiction
            cause.append(root)
        else:
            # check if one of the caused assignment has caused the contradiction
            cause = cause + get_causes(r, root.caused_list)

    return cause

def get_root_cause(r):
    """
    this function get a cause and return the root of this cause, if the cause is a  root assignment return himself, else recursive call is used
    :param r: cause to be determined the root
    :return:
    """
    root = []

    if r.causes_list:
        for causes in r.causes_list:
            root = root + get_root_cause(causes)

    else:
        return r

    return root
