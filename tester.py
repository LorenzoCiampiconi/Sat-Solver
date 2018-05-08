import file_handler
import solver
from sat_problem_objects import Formula
import numpy as np

def test():
    formula = Formula()
    formula = file_handler.read_files(formula)

    random_calls = []
    random_assignments = []
    heuristic_calls = []
    heuristic_assignments = []

    for i in range(250):

        time, assignments, correct = solver.solve(formula, True)
        random_calls.append(time)
        random_assignments.append(assignments)
        time, assignments, correct = solver.solve(formula, False)
        heuristic_calls.append(time)
        heuristic_assignments.append(assignments)
    
    print("heuristic medium calls: " + str(np.mean(heuristic_calls)))
    print("heuristic medium number of assignments: " + str(np.mean(heuristic_assignments)))
    print("correctness: " + str(len(heuristic_calls)/250))
    print("random medium: " + str(np.mean(random_calls)))
    print("random medium number of assignments: " + str(np.mean(random_assignments)))
    print("correctness: " + str(len(heuristic_calls) / 250))

test()