N = 5

from sat_problem_objects import Formula, Clause


def generate_puzzle():

    clauses = []
    number_of_var = 0

    # adding attributes

    # NATIONALITIES
    # in order
    # BRIT x1 to x5
    # SWEDE x6 to x10
    # DANE x11 to x15
    # NORVEGIAN x16 to x20
    # GERMAN x21 to x 25
    new_clauses, added_var = exclusive_attribute(number_of_var)

    clauses += new_clauses
    number_of_var += added_var

    # COLORS
    # in order
    # RED x26 to x30
    # WHITE x31 to x35
    # YELLOW x36 to x40
    # GREEN x41 to x45
    # BLUE x46 to x50
    new_clauses, added_var = exclusive_attribute(number_of_var)

    clauses += new_clauses
    number_of_var += added_var

    # CIGARETTES
    # in order
    # PALLMALL x51 to x55
    # DUNHILL x56 to x60
    # BLENDS x61 to x65
    # PRINCE x66 to x70
    # BLUEMASTER x71 to x75
    new_clauses, added_var = exclusive_attribute(number_of_var)

    clauses += new_clauses
    number_of_var += added_var

    # DRINKS
    # in order
    # TEA x76 to x80
    # MILK x81 to x85
    # COFFEE x86 to x90
    # BEER x91 to x95
    # WATER x96 to x100
    new_clauses, added_var = exclusive_attribute(number_of_var)

    clauses += new_clauses
    number_of_var += added_var

    # PETS
    # in order
    # CATS x101 to x105
    # DOGS x106 to x110
    # BIRDS x111 to x115
    # HORSE x116 to x120
    # FISH x121 to x125
    new_clauses, added_var = exclusive_attribute(number_of_var)

    clauses += new_clauses
    number_of_var += added_var


    # ************* ADDING HINTS *************

    # associate brit and red house
    a_var = list(range(1,6))
    b_var = list(range(26,31))

    new_clauses =  associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate swede and dogs
    a_var = list(range(6, 11))
    b_var = list(range(106,111))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate Dane and Tea
    a_var = list(range(11, 16))
    b_var = list(range(76, 81))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate Green and Coffee
    a_var = list(range(41, 46))
    b_var = list(range(86, 91))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate Pall Mall and Birds
    a_var = list(range(51, 56))
    b_var = list(range(111, 116))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate Yellow and Dunhill
    a_var = list(range(36, 41))
    b_var = list(range(56, 61))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate Bluemaster and Beer
    a_var = list(range(71, 76))
    b_var = list(range(91, 96))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # associate German and Prince
    a_var = list(range(21, 26))
    b_var = list(range(66, 71))

    new_clauses = associates_attributes(b_var, a_var)
    clauses += new_clauses

    # Norvegian lives in the first house
    clauses += [Clause([16])]

    # Milk in the center house
    clauses += [Clause([83])]

    # Green on the left of white
    a_var = list(range(31, 36))
    b_var = list(range(41, 46))
    clauses += is_on_the_left(a_var, b_var)

    # Blends next to Cats
    a_var = list(range(61, 66))
    b_var = list(range(101, 106))
    clauses += lives_next(a_var, b_var)

    # Horse next to Dunhill
    a_var = list(range(116, 121))
    b_var = list(range(56, 61))
    clauses += lives_next(a_var, b_var)

    # Norvegian next to Blue
    a_var = list(range(16, 21))
    b_var = list(range(46, 51))
    clauses += lives_next(a_var, b_var)

    # Norvegian next to Blue
    a_var = list(range(16, 21))
    b_var = list(range(46, 51))
    clauses += lives_next(a_var, b_var)

    # Blends next to Water (has neighbour same as lives next to)
    a_var = list(range(61, 66))
    b_var = list(range(96, 111))
    clauses += lives_next(a_var, b_var)

    formula = Formula()
    formula.clauses = clauses
    formula.v = number_of_var
    formula.nc = len(clauses)

    return formula


def exclusive_attribute(last_var):

    new_var = 0

    clauses = []

    # last assigned var
    j = last_var + 1

    # for each person it can only have one attribute
    for i in range(N):
        # at least one true
        clause = [j, j + 1, j + 2, j + 3, j + 4]
        clauses.append(Clause(clause))

        # positional xor
        for k in range(N - 1):
            for l in range(0, N - k):
                if j + k != j + k + l:
                    clause = [-(j + k), -(j + k + l)]
                    clauses.append(Clause(clause))

        j = j + N

    # last assigned var
    j = last_var + 1

    # for each attribute it can only belong to a person
    # exclusive xor
    for i in range(N - 1):
        for k in range(N):
                var = j + k
                for l in range(N - i):
                    m = var + l*N

                    if m != var:
                        clause = [-var, -m]
                        clauses.append(Clause(clause))

        j = j + N

    added_var = N * N

    return clauses, added_var


def associates_attributes(list1, list2):

    concat = [list1, list2]

    # transform in cnf (A && B) || (C && D) || (E && F) || (G && J) || (H && I)
    new_clauses = recursive_combination(list1, list2)

    clauses = []
    for clause in new_clauses:
        clauses.append(Clause(clause))

    return clauses


def recursive_combination(list1, list2):

    if len(list1) > 1:
        results = recursive_combination(list1[1:], list2[1:])

        new_comb = []

        for result in results:
            new_comb.append([list1[0]] + result)
            new_comb.append([list2[0]] + result)

        return new_comb

    else:
        return [[list1[0]], [list2[0]]]


# 1 is on the left of 2
def is_on_the_left(list1, list2):

    clauses = []
    for i in range(N - 1):
        clause = [list1[i]] + [list2[i+1]]
        clauses.append(Clause(clause))

    for clause in clauses:
        print(clause.c)

    return clauses


# lives next means or list 1 is on the left of list2, or list2 is on the left of list1
def lives_next(list1, list2):

    clauses = is_on_the_left(list1, list2)
    clauses += is_on_the_left(list2, list1)

    return clauses

generate_puzzle()
