from Formula import Formula

#Define path and useful variables such as the separator used in the file to be queried
read_path = "/home/lorenzoc/Scrivania/Sat-Solver/"
output_path = "/home/lorenzoc/Scrivania/Sat-Solver/"
query_list_file_name = "input"
output_file_name = "outputB.txt"
sep = "\t"





# This function get the formula from a file respecting DIMACS CNF standard
def read_files():

    #open the file
    with open(read_path + query_list_file_name, "r") as input_file:
        formula = Formula()

        for line in input_file:
            if line.startswith("c"):
                print(line.partition("c")[2])
            elif line.startswith("p cnf"):
                words = line.split(" ")
                formula.v = int(words[2])
                formula.nc = int(words[3])
            else :
                clause = line.partition(" 0")[0]
                clause = clause.split()
                formula.c.append(list(map(int, clause)))

    return formula




