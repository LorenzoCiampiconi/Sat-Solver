import logic_functions as lf
import assignments_graph as ag
import cdcl
from sat_problem_objects import Formula

GENERATION = True
CONTRADICT = False
EMPTY = []


class Watcher:
    def __init__(self, lit):
        """
        constructor for class Watcher
        the class has the aim to represent a watcher to a literal in a clause,
        when an assignment is done (i.e. -3) then every clause watched (with 3)
        is verified
        the structure is lazy as only two literal for clause has been watched
        :param lit:
        """
        self.watched = []  # watched clauses with the opposite literal
        self.literal = lit

    def add_watched_clause(self, clause):
        """
        add a clause to be watched to a watcher
        :param clause: the actual clause to be watched
        """
        self.watched.append(clause)

    def remove_watched_clause(self, clause):
        """
        remove a clause that has been watched from a watcher
        :param clause: the actual clause that was watched
        """
        self.watched.remove(clause)


def generate_watch_list(formula: Formula):
    """
    Generate random watch-list with 2 variable watched for each clause
    :param formula: Formula input to SAT-SOLVER
    :return:
    """
    watch_list = []

    # generate 2*n watcher (one for i, one for ~i)
    for i in range(1, formula.v + 1):

        # create watcher for both possible assignment (i and ~i)
        watcher = Watcher(i)
        watch_list.append(watcher)

        watcher = Watcher(-1 * i)
        watch_list.append(watcher)

    # assigned two variables of the clause to relative watch list
    for clause in formula.clauses:

        add_clause_to_watch_list(clause, watch_list, GENERATION, EMPTY)

    return watch_list


def add_clause_to_watch_list(clause, watch_list, generation, a):

    # if this is for the generation of a watch_list then two variables must be watched
    if generation:
        # shuffle order of the formula
        clause.shuffle()
        # add the first two (opposite) random literal to watch list
        lit = -1 * clause.get_first_literal()  # clause must be watched when assignment is opposite
        watch_list[index_of_literal(lit)].add_watched_clause(clause)

        if len(clause.c) > 1:
            lit = -1 * clause.get_second_literal()  # clause must be watched when assignment is opposite
            watch_list[index_of_literal(lit)].add_watched_clause(clause)

    # if the assignment ar relevant as the clause is learnt
    elif a:
        clause.watched_and_move(a)
        # add the first two (opposite) random literal to watch list
        lit = -1 * clause.get_first_literal()  # clause must be watched when assignment is opposite
        watch_list[index_of_literal(lit)].add_watched_clause(clause)
        if len(clause.c) > 1:
            lit = -1 * clause.get_second_literal()  # clause must be watched when assignment is opposite
            watch_list[index_of_literal(lit)].add_watched_clause(clause)

    # if not, then this mean that a variable was watched, then a new one must be watched
    # the last variable watched will be moved to the rear of the clause
    else:
        lit = -1 * clause.get_second_literal()  # clause must be watched when assignment is opposite
        watch_list[index_of_literal(lit)].add_watched_clause(clause)

        # print("new literal: " + str(lit))


def index_of_literal(literal):
    """
    this function is to assign an index on the basis of the literal
    :param literal: which literal i should retrieve the index of
    :return:
    """
    # watch list is ordered in monotone order with positive in even position, and negative in odd position
    # i.e [1, -1, 2, -2, 3, -3..., n, -n]
    # so index of 1 ---> (2-2) = 0
    # index of -3 ---> (6 -2 +1) = 5
    return abs(literal) * 2 - 2 + (1 if literal < 0 else 0)


def watch_a_literal(lit, sp, level):
    """
    induct a new assignment to lit, considering all the assignment a
    as we are watching only two literal for a clause
    :param sp:
    :param level: level of the assignment of lit
    :param lit: literal to be watch
    """

    # retrieve watcher for  literal
    watcher = sp.watch_list[index_of_literal(lit)]

    temp = []

    for clause in watcher.watched:

        if not lf.is_satisfied(clause, sp.a):

            # print("has not being sat and")
            clause.is_not_sat() # set the fact that the clause has not been satisfied

            # keep track of every literal that has been watched
            if clause.watched_and_move(sp.a) > 1:  # if there's more than one literal

                temp.append(clause)

                # add next literal to the watch list
                add_clause_to_watch_list(clause, sp.watch_list, not GENERATION, EMPTY)

            elif clause.n_ass == 1:

                clause.is_sat()  # set the fact that the clause has been satisfied

                causes = [-1 * lit for lit in clause.c[1:]]

                ag.define_assignment(clause.get_first_literal(), sp, causes, level, clause)

                not_contradict, backtrack = watch_a_literal(clause.get_first_literal(), sp, level)

                if not not_contradict:

                    for item in temp:
                        watcher.watched.remove(item)
                    return not_contradict, backtrack

            else:

                for item in temp:
                    watcher.watched.remove(item)

                r = lf.assign_to_clause(clause, sp.a)
                return CONTRADICT, cdcl.learning_clause(r, clause, sp, level)

        else:
            # print("clause is sat")
            clause.is_sat()  # set the fact that the clause has been satisfied

    for item in temp:
        watcher.watched.remove(item)

    # no contradiction has been found while watching this literal
    return not CONTRADICT, EMPTY





