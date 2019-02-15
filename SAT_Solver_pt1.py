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
    puzzle_history = puzzle.copy()  # to keep track of back-tracking

    var_list = []   #for pure literal simplificatoin
    for clause in puzzle:
        if unit_switch == 1:
            if len(clause) == 1:
                for var in clause:
                    if var<0:
                        FinalSoln[abs(var)] = -1
                    else:
                        FinalSoln[var] = 1
        for var in clause:
            if tautology_switch ==1:
                if -1 * var in clause:
                    puzzle.remove(clause)
            if pure_switch == 1:
                var_list.append(var)

    if pure_switch == 1:
        for var in var_list:
            if -1 * var not in var_list:
                if var < 0:
                    FinalSoln[abs(var)] = -1
                else:
                    FinalSoln[var] = 1

    return puzzle_history, FinalSoln, puzzle

# ----------Splitting----------
def split(FinalSoln,Heuristic):
    if Heuristic == 'random':
        split_var = random.choice(list(FinalSoln.keys()))
        split_val = random.randint(0,1)
    FinalSoln[split_var] = split_val
    return FinalSoln, split_val, split_var

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

# ----------Back Tracking----------
def back_track(puzzle_history,FinalSoln,split_val,split_var):
    # changing the truth value
    FinalSoln[split_var] = -1*split_val
    # backtracking in puzzle
    puzzle = puzzle_history

    return puzzle,FinalSoln

#add other types of backtracking

# ----------Main----------
tautology_switch = 1
pure_switch = 1
unit_switch = 1
Heuristic = 'random'
puzzle_history, FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
stop_check = stop(puzzle, FinalSoln)
tautology_switch = 0
a=1
while stop_check == 0:
    FinalSoln,split_val,split_var = split(FinalSoln, Heuristic)
    puzzle_history, FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
    stop_check = stop(puzzle, FinalSoln)
    if stop_check == 0:
        puzzle, FinalSoln = back_track(puzzle_history,FinalSoln,split_val,split_var)
    print('iter',a)
    print(len(puzzle))
    a +=1

