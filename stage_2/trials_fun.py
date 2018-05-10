import random
import subprocess as sbp
from sat_problem_objects import Formula, Clause

COMMENT = "c randomly generated \n" + "c \n"
END_LINE_CHAR = "0\n"
COMMAND = "./minisat"
INPUT = "input"
OUTPUT = "output"
SAT_OUTPUT = "SAT\n"
UNSAT_OUTPUT = "UNSAT\n"
RESULTS = "saved_results"
EMPTY_DIR = ''
# fixed parameters
N = 150
SIGN = [-1, 1]
N_TRIALS = 50
K = [3, 4, 5]
HOP = 0.2
MAX_R = 8.8


def generate_formula(n, r, k):

    formula = Formula()
    formula.v = n
    formula.nc = int(r*n)

    for i in range(int(r*n)):
        clause = [random.sample(SIGN, 1)[0] * var for var in random.sample(list(range(1, n + 1)), k)]
        formula.clauses.append(Clause(clause))

    return formula


def generate_cnf_file(n, r, k):

    formula = generate_formula(n, r, k)

    write_cnf_file(formula, n, int(r*n), directory)


def write_cnf_file(formula, n, c, directory):

    with open(directory + INPUT, "+w") as input_file:
        input_file.write(COMMENT)
        input_file.write("p cnf " + str(n) + " " + str(c) + "\n")

        for clause in formula.clauses:
            clause_string = ''
            for lit in clause.c:
                clause_string += str(lit) + " "
            clause_string += "0\n"
            input_file.write(clause_string)


def verify_with_mini_sat(formula, directory):
    write_cnf_file(formula, formula.v, formula.nc, directory)
    sbp.run([directory + COMMAND, directory + INPUT, directory + OUTPUT], stdout=sbp.PIPE)
    return is_sat_by_mini(directory)


def is_sat_by_mini(DIR):

    with open(DIR + OUTPUT, "r") as output_file:

        for line in output_file:

            if line == SAT_OUTPUT:
                return True

            elif line == UNSAT_OUTPUT:
                return False