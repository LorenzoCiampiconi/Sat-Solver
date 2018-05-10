import subprocess as sbp
import numpy as np
import random
import time
from stage_2 import printer
from stage_2 import trials_fun as tr
from sat_problem_objects import Formula

COMMENT = "c randomly generated \n" + "c \n"
END_LINE_CHAR = "0\n"
COMMAND = "./minisat"
INPUT = "input"
OUTPUT = "output"
SAT_OUTPUT = "SAT\n"
UNSAT_OUTPUT = "UNSAT\n"
RESULTS = "saved_results"
RELATIVE_DIR = ''
# fixed parameters
N = 150
SIGN = [-1, 1]
N_TRIALS = 50
K = [3, 4, 5]
HOP = 0.2
MAX_R = 8.8


def trials():

    # list of probability of SAT
    number_of_clauses = np.arange(0, MAX_R + HOP, HOP)

    p_of_sat = []
    cpu_time = []

    for k in K:
        p = []
        cpu_t = []
        print("k = " + str(k))
        for r in number_of_clauses:
            counter = 0
            print("r = " + str(r))
            temp_time = []
            for t in range(N_TRIALS):
                tr.generate_cnf_file(N, r, k)

                ti = time.time()
                sbp.run([COMMAND, INPUT, OUTPUT], stdout=sbp.PIPE)
                ti = time.time() - ti
                temp_time.append(ti)

                if tr.is_sat_by_mini(RELATIVE_DIR):
                    counter += 1

            cpu_t.append(np.mean(temp_time))
            p.append(counter/N_TRIALS)

        p_of_sat.append(p)
        cpu_time.append(cpu_t)

    # obtain actual number of clauses from the ratio r
    number_of_clauses = [int(r * N) for r in number_of_clauses]

    save_results(p_of_sat, cpu_time)

    print("printing")
    printer.plot_probability_and_time(K, number_of_clauses, p_of_sat, cpu_time)


def save_results(p_of_sat, cpu_time):

    with open(RESULTS, "+w") as results_file:

        results_file.write(str(p_of_sat) + "\n")
        results_file.write(str(cpu_time) + "\n")

trials()
