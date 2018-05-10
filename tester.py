import file_handler
import solver
from sat_problem_objects import Formula
from stage_2 import trials_fun as tr
import numpy as np
import random
import time
import copy
from matplotlib import pyplot as plt


DIR = "stage_2/"
TRIALS = 40
N = 100
R = 7
K = 3


def test():

    formula = Formula()
    formula, valid_input = file_handler.read_files(formula, input=False)

    random_calls = []
    random_assignments = []
    random_time = []
    heuristic_calls = []
    heuristic_assignments = []
    heuristic_time = []

    for i in range(250):

        t = time.time()
        calls, assignments, correct = solver.solve(formula, True)
        t = time.time() - t
        random_calls.append(calls)
        random_assignments.append(assignments)
        random_time.append(t)

        t = time.time()
        calls, assignments, correct = solver.solve(formula, False)
        t = time.time() - t
        heuristic_time.append(t)
        heuristic_calls.append(calls)
        heuristic_assignments.append(assignments)
    
    print("heuristic medium calls: " + str(np.mean(heuristic_calls)))
    print("heuristic medium number of assignments: " + str(np.mean(heuristic_assignments)))
    print("correctness: " + str(len(heuristic_calls)/250))
    print("random medium: " + str(np.mean(random_calls)))
    print("random medium number of assignments: " + str(np.mean(random_assignments)))
    print("correctness: " + str(len(heuristic_calls) / 250))


def test_sat_unsat():

    random_calls = []
    random_assignments = []
    random_time = []
    heuristic_calls = []
    heuristic_assignments = []
    heuristic_time = []

    i = 0
    while i < TRIALS:

        formula = tr.generate_formula(N, R, K)

        if not tr.verify_with_mini_sat(formula, DIR):

            # test Random
            t = time.time()
            calls, assignments, correct = solver.solve(formula, True)
            t = time.time() - t
            random_calls.append(calls)
            random_assignments.append(assignments)
            random_time.append(t)

            # test Heuristic
            t = time.time()
            calls, assignments, correct = solver.solve(formula, False)
            t = time.time() - t
            heuristic_time.append(t)
            heuristic_calls.append(calls)
            heuristic_assignments.append(assignments)

            i += 1

        else:
            print("not UNSAT")

    print("heuristic medium calls: " + str(np.mean(heuristic_calls)))
    print("heuristic medium number of assignments: " + str(np.mean(heuristic_assignments)))
    print("heuristic medium time: " + str(np.mean(heuristic_time)))

    print("random medium: " + str(np.mean(random_calls)))
    print("random medium number of assignments: " + str(np.mean(random_assignments)))
    print("random medium time: " + str(np.mean(random_time)))



def test_heuristic(n):

    random_calls = []
    random_assignments = []
    random_time = []
    heuristic_calls = []
    heuristic_assignments = []
    heuristic_time = []

    for i in range(TRIALS):

        formula = tr.generate_formula(n, R, K)

        input = copy.deepcopy(formula)

        # test Random
        t = time.time()
        calls, assignments, correct = solver.solve(input, True)
        t = time.time() - t
        random_calls.append(calls)
        random_assignments.append(assignments)
        random_time.append(t)

        # test Heuristic
        t = time.time()
        calls, assignments, correct = solver.solve(formula, False)
        t = time.time() - t
        heuristic_time.append(t)
        heuristic_calls.append(calls)
        heuristic_assignments.append(assignments)

    print("heuristic medium calls: " + str(np.mean(heuristic_calls)))
    print("heuristic medium number of assignments: " + str(np.mean(heuristic_assignments)))
    print("heuristic medium time: " + str(np.mean(heuristic_time)))

    print("random medium: " + str(np.mean(random_calls)))
    print("random medium number of assignments: " + str(np.mean(random_assignments)))
    print("random medium time: " + str(np.mean(random_time)))

    return np.mean(heuristic_calls), np.mean(heuristic_assignments), np.mean(random_calls), np.mean(random_assignments)


def varying_n():

        n = [50, 80]
        hop = 3

        HC = []
        HA = []
        RC = []
        RA = []

        for n_i in range(50, 80 + hop, hop):
            hc, ha, rc, ra = test_heuristic(n_i)

            HC.append(hc)
            HA.append(ha)

            RC.append(rc)
            RA.append(ra)

        x = list(range(50, 80 + hop, hop))

        plt.title("Comparison of heuristic with number of call of subroutine in function of n")
        plt.plot(x, HC, "ro", label="Heuristic")
        plt.plot(x, HC, "r")
        plt.plot(x, RC, "yo", label="Random")
        plt.plot(x, RC, "y")
        plt.xlabel("number of variables")
        plt.ylabel("call of subroutine")
        plt.legend(loc="upper left")
        plt.savefig("comparison-call-subroutine.png")
        plt.show()

        plt.title("Comparison of heuristic with number of assignments in function of n")
        plt.plot(x, HA, "ro", label="Heuristic")
        plt.plot(x, HA, "r")
        plt.plot(x, RA, "yo", label="Random")
        plt.plot(x, RA, "y")
        plt.xlabel("number of variables")
        plt.ylabel("number of assignments")
        plt.legend(loc="upper left")
        plt.savefig("comparison-number-assignments.png")
        plt.show()



varying_n()