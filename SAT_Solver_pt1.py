import random


def readDIMACS(filename):
    """
    convert DIMACS file into list of numbers

    :param filename:
    :return: list
    """

    myList = []
    f = open(filename, "r")
    for line in f:
        line = line.split()
        # Use 'try' and 'except' to skip over any non-integer lists
        try:
            line = list(map(int, line))
            line = line[0:len(line) - 1]  # removes zero from the end of each line
            myList.append(line)
        except:
            pass

    return myList


# To initialize our problem
myRulesList = readDIMACS('sudoku-rules.txt')
myPuzzle = readDIMACS('sudoku-example.txt')
puzzle = myRulesList + myPuzzle

# To initialize 'blank' soln
FinalSoln = {}
for i in puzzle:
    for j in i:
        FinalSoln[abs(j)] = 0   #They are initialized as 0, true is 1 and false is -1

# ----------Simplification----------
def simplify(puzzle,FinalSoln,tautology_switch, pure_switch, unit_switch):
    """

    :param puzzle:
    :param FinalSoln:
    :param tautology_switch:
    :param pure_switch:
    :param unit_switch: puts clauses of size one to true
    :return:
    """

    stop_simplifying_check = 1
    while stop_simplifying_check == 1:   #stops when nothing has changed in the last simplification
        var_list = []   # for pure literal simplification
        for clause in puzzle:
            for var in clause:
                # tautology
                if tautology_switch == 1:
                    if -1 * var in clause:
                        puzzle.remove(clause)
                        stop_simplifying_check = 0
                # unit clause
                if unit_switch == 1:
                    if len(clause) == 1:
                        if var < 0:
                            FinalSoln[abs(var)] = -1
                        else:
                            FinalSoln[var] = 1
                        puzzle.remove(clause)
                        stop_simplifying_check = 0
                # pure
                if pure_switch == 1:
                    var_list.append(var)

        if pure_switch == 1:
            for var in var_list:
                if -1 * var not in var_list:
                    stop_simplifying_check = 0
                    if var < 0:
                        FinalSoln[abs(var)] = -1
                    else:
                        FinalSoln[var] = 1
        # omitting the assigned variables from clauses and empty clauses
        for clause in puzzle:
            if len(clause) == 0:
                puzzle.remove(clause)
                stop_simplifying_check = 0
            for var in clause:
                if FinalSoln[abs(var)] != 0:
                    clause.remove(var)
                    stop_simplifying_check = 0

    return FinalSoln, puzzle

# ----------Splitting----------
def split(FinalSoln, chosen_list, Heuristic):
    # we can only split those that are not assigned yet
    vars_to_split = []
    for var in FinalSoln:
        if FinalSoln[var] != 0:
            vars_to_split.append(var)

    backtrack_to = 0    # backtrack_to =0: there is nothing to backtrack to, another variable is chosen in the same branch
    if len(vars_to_split) == 0: # no split options left, have to back track
        for var in reversed(chosen_list):
            if FinalSoln[var] == 1:
                FinalSoln[var] = -1
                backtrack_to = var
                break
        if backtrack_to == 0:
            backtrack_to = -1   # the puzzle is inconsistent
    else:
        if Heuristic == 'random':
            split_var = random.choice(vars_to_split)

        FinalSoln[split_var] = 1


    return FinalSoln, split_var, backtrack_to

# ----------Stopping----------
def stop(puzzle,FinalSoln):
    found_solution = 1
    for clause in puzzle:
        clause_sat = 0
        for var in clause:
            if FinalSoln[abs(var)] == 1:
                clause_sat = 1
        if clause_sat == 0:
            found_solution = 0
            break
    return found_solution
#add inconsistant


# ----------Main----------
tautology_switch = 1
pure_switch = 1
unit_switch = 1
Heuristic = 'random'
FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
stop_check = stop(puzzle, FinalSoln)
tautology_switch = 0
a=1
while stop_check == 0:
    chosen_list = []
    FinalSoln, split_var, backtrack_to = split(FinalSoln, chosen_list, Heuristic)
    puzzle_history = puzzle.copy()  # to keep track of back-tracking
    FinalSoln_history = FinalSoln.copy()
    if backtrack_to == 0:
        FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
    else:

    stop_check = stop(puzzle, FinalSoln)
    if stop_check == 0:
        puzzle, FinalSoln = back_track(puzzle_history,FinalSoln,split_var)
    print('iter',a)
    print(len(puzzle))
    a +=1

