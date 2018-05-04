import random
import numpy as np
import watch_list as wl


class SatProblem:
    def __init__(self):
        # todo
        c = []


class Formula:

    def __init__(self):
        self.v = ''  # number of variable
        self.nc = ''  # number of clauses
        self.clauses = []  # list of clauses
        self.counter = ''

    def count_unsat(self):
        self.counter = sum([1 for clause in self.clauses if not clause.sat])
        return self.counter

    def add_learnt_clause(self, learnt_clause, a, watch_list):
        self.clauses.append(learnt_clause)
        wl.add_clause_to_watch_list(learnt_clause, watch_list, not wl.GENERATION, a)


class Clause:

    def __init__(self, c):
        self.c = c
        self.n_ass = len(c)
        self.sat = False

    def shuffle(self):
        self.c = random.sample(self.c, len(self.c))

    def watched_and_move(self, a):
        """
        This fuction is supposed to be called when this clause has not been SAT yet
        This count the number of the assignment done to the literal constraint by this clause
        Move all of those literal to the rear
        :param a: actual assignments
        """

        abs_a = np.abs(a)

        count = 0
        i = 0
        for lit in self.c[:]:
            # count literal that has been assigned of this not yet assigned clause, move those literals to the rear
            if abs(lit) in abs_a :
                self.c = self.c[:i] + self.c[i + 1:] + [self.c[i]]
                count += 1

            i += 1

        self.n_ass = len(self.c) - count
        return self.n_ass

    def get_first_literal(self):
        return self.c[0]

    def get_second_literal(self):
        return self.c[0]

    def is_sat(self):
        self.sat = True

    def is_not_sat(self):
        self.sat = False



        