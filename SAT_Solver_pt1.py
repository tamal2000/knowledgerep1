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

# ----------Heuristics--------------
def JW_onesided(myPuzzle, potentialVarsList):

    """
    :param myPuzzle: The list of rules you're trying to solve
    :param potentialVarsList: List of variables we can select from
    :return: selectedVar
    """

    # Initializing dictionary of potentialVariable: variableWeight from a list of possible variables
    varWeights = {}
    for myVar in potentialVarsList:
        varWeights[myVar] = 0

    # Search the entire puzzle for all occurrences of variable
    for clause in myPuzzle:
        # Checks to see the clause contains
        for puzzleVar in clause:
            # checks to see if any variables from potentialVarsList are in that specific clause of the puzzle
            # if so, update the varweight using the JW formula
            if (puzzleVar in potentialVarsList) == True:
                varWeights[abs(puzzleVar)] += 2**(-1*len(clause))

    # Following part addresses scenario in which several vars share the maximum weight
    # Will build a list of all vars with max value, then randomly select a var to be returned
    maxVal = max(varWeights.values())
    selectionList = []
    for myVar, myVarWeight in varWeights.items():
        if myVarWeight == maxVal:
            selectionList.append(myVar)
    selectedVar = random.choice(selectionList)

    return selectedVar

def DLIS(myPuzzle, potentialVarsList, currentSoln): # Pass me the puzzle
    """
    Counts the number of occurrences of literal l in unsatisfied clauses. Returns l with highest count.

    :param myPuzzle: The current state of the puzzle.
    :param potentialVarsList: List of variables to consider for selection
    :param currentSoln:The assigned truth values for all variables in entire puzzle.

    :return: selectedVar: The variable (from potentialVarsList) that yields the most unsatisfied clauses.
    """

    # Initializing dictionary of potentialVariable: variableWeight from a list of possible variables
    varWeights = {}
    for myVar in potentialVarsList:
        varWeights[myVar] = 0

    for clause in myPuzzle:
        # converts list of clauseVars to list of truth assignments
        clauseValues = []
        for myVar in clause:
            if myVar >= 0:
                clauseValues.append(currentSoln[abs(myVar)])
            # Calculates the negation for a particular var
            else:
                clauseValues.append(-1 * currentSoln[abs(myVar)])
        # if clause not satisfied, then check to see if variables from varList are in it
        if (1 in clauseValues) == False:
            for myVar in potentialVarsList:
                if (myVar in clause) == True:
                    varWeights[myVar] += 1

    # Selects variable with highest occurrence of unsatisified clauses.
    # If there's a tie, one variable is randomly selected.
    maxVal = max(varWeights.values())
    selectionList = []
    for myVar, myVarWeight in varWeights.items():
        if myVarWeight == maxVal:
            selectionList.append(myVar)
    selectedVar = random.choice(selectionList)

    return selectedVar

# ----------Simplification----------
def simplify(puzzle,FinalSoln,tautology_switch, pure_switch, unit_switch):
    """

    :param puzzle:
    :param FinalSoln:
    :param tautology_switch:
    :param pure_switch:
    :param unit_switch: puts clauses of size one to true
    :return: FinalSoln, puzzle (puzzle only contains unsatisfied clauses)
    """

    stop_simplifying_check = 0
    while stop_simplifying_check == 0:   #stops when nothing has changed in the last simplification
        stop_simplifying_check = 1
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
            else:
                for var in clause:
                    if FinalSoln[abs(var)] != 0:
                        if FinalSoln[abs(var)]*var > 0: #remove satisfied clause
                            puzzle.remove(clause)
                            stop_simplifying_check = 0
                            break
                        else:   #romoves assigned variable form clause
                            clause.remove(var)
                            stop_simplifying_check = 0

    return FinalSoln, puzzle

# ----------Splitting----------
def split(FinalSoln, puzzle, FinalSoln_history, puzzle_history, chosen_list, Heuristic):
    # we can only split those that are not assigned yet
    vars_to_split = []
    for var in FinalSoln:
        if FinalSoln[var] == 0:
            vars_to_split.append(var)

    backtrack_to = 0    # backtrack_to =0: there is nothing to backtrack to, another variable is chosen in the same branch
    if len(vars_to_split) == 0: # no split options left, have to back track
        for var in reversed(chosen_list):
            if FinalSoln[var] == 1:
                puzzle = puzzle_history[var]
                FinalSoln = FinalSoln_history[var]
                FinalSoln[var] = -1
                backtrack_to = var
                break
        if backtrack_to == 0:
            backtrack_to = -1   # the puzzle is inconsistent
    else:
        if Heuristic == 'random':
            split_var = random.choice(vars_to_split)
        if Heuristic == 'JW_onesided':
            split_var = JW_onesided(puzzle, vars_to_split)
        if Heuristic == 'DLIS':
            split_var = DLIS(puzzle, vars_to_split, FinalSoln)
        puzzle_history[split_var] = puzzle.copy()
        FinalSoln_history[split_var]= FinalSoln.copy()
        FinalSoln[split_var] = 1
        chosen_list.append(split_var)



    return FinalSoln, puzzle, puzzle_history, FinalSoln_history, chosen_list, backtrack_to

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
Heuristic = 'JW_onesided'
FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
stop_check = stop(puzzle, FinalSoln)
tautology_switch = 0
a=1
while stop_check == 0:
    chosen_list = []
    puzzle_history = {}
    FinalSoln_history = {}
    FinalSoln, puzzle, puzzle_history, FinalSoln_history, chosen_list, backtrack_to = split(FinalSoln,
                                                                                            puzzle, FinalSoln_history,
                                                                                            puzzle_history, chosen_list,
                                                                                            Heuristic)
    if backtrack_to == -1:  # the problem is inconsistent
        stop_check = -1
    FinalSoln, puzzle = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
    stop_check = stop(puzzle, FinalSoln)
    if stop_check == 1:
        print(FinalSoln)

    print('iter',a)
    print(len(puzzle))
    a +=1

