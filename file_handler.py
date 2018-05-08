# Define path and useful variables such as the separator used in the file to be queried
read_path = "input-test-files"
query_list_file_name = "/input-4"
extension = ".cnf"
sep = "\t"

from sat_problem_objects import Clause


# This function get the formula from a file respecting DIMACS CNF standard
def read_files(formula):

    # open the file
    with open(read_path + query_list_file_name, "r") as input_file:

        for line in input_file:
            if line.startswith("c"):
                print(line.partition("c")[2])
            elif line.startswith("p cnf"):
                words = line.split(" ")
                formula.v = int(words[2])
                formula.nc = int(words[3])

            else:
                clause = line.partition(" 0")[0]
                clause = clause.split()
                clause = Clause(list(set(map(int, clause))))
                formula.clauses.append(clause)

    return formula




