import random
import time
from copy import deepcopy

def readDIMACS(filename,sudokuNum=None):
    """
    convert DIMACS file into list of numbers. There's an if-else statement that acts as a switch to see whether
    you're inputting a list of rules OR the non-DIMACS version of Sudoku puzzle. If it's a non-DIMACS Sudoku puzzle,
    it call the function getMySudoku(filename, sudokuNum).

    :param filename:
    :return: list
    """

    # Processes the rules List
    if sudokuNum == None:
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
    # Pulls a DIMACS version of the Sudoku list and outputs it in same format as Sudoku rules (so you can concatonate the
    # two list later on)
    else:
        myList = []
        DIMACS_Lines = getMySudoku(filename, sudokuNum)
        for index in range(len(DIMACS_Lines)):
            makelineList = []
            line = DIMACS_Lines[index]
            #line = list(map(int, line))
            line = line[0:len(line) - 2]  # removes zero AND whitespace from the end of each line
            line = int(line)
            makelineList.append(line)
            myList.append(makelineList)
    return myList

def getMySudoku(filename, sudokuNum):
    """
    :param filename: The filename of mega-Sudoku text file.
    :param sudokuNum: The number of the Sudoku puzzle you want to retrieve. sudokuNum ranges from 0 to len(filename)/81.
    If the Sudoku puzzle number supplied is out of bounds, you'll recieve an error message.

    :return: 0 : Returns a list of DIMACS lines to be processed in the readDIMACS function
    """

    # Opening the mega-Sudoku file as a single string of text
    with open(filename, "r") as myfile:
        fileText = myfile.read()
    # Splitting the file into the Sodoku puzzle you want
    """
    For some reason, there are random '\n' in text file...if you don't remove them, the file won't be parsed correctly....
    It took me an hour to figure out that was the problem. Though, I don't fully understand why, so if you're feeling
    extra motivated, you can look it over.
    """
    fileText = fileText.replace("\n", "")
    if len( fileText)/81 >=  sudokuNum:
        puzzle = fileText[sudokuNum*81 : sudokuNum*81 + 81]


        # Convert flat list into ordered list to access numbers
        puzzleRows = [puzzle[i:i+9] for i in range(0, len(puzzle), 9)]
        # Then use ordered list to extract (Row,Col,GridValue) and output DIMACS file
        DIMACS_lines = []
        for index in range(len(puzzleRows)):
            puzzleRows[index] = list(puzzleRows[index])
            for gridIndex, gridValue in enumerate(puzzleRows[index]):
                if gridValue != '.':
                    DIMACS_line = str(index+1)+str(gridIndex+1) + str(gridValue) + str(' 0')
                    DIMACS_lines.append(DIMACS_line)
    else:
        print("Error. Puzzle doesn't exist. Try inputting a smaller, non-negative number.")

    return DIMACS_lines


# Inconsistent puzzles: 12, 16, 20, 22, 23, 24, 27, 30 from the 1,000 Sudoku
# myPuzzle = readDIMACS('top91.sdk.txt', 0)
# print(myPuzzle)
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
    simplifies the puzzle by omitting tautologies, setting pure literals to 1, and omitting unit clauses and setting
    them to 1. It omits all the variables that are assigned in the FinalSoln from the puzzle to save time in future
    computations.
    :param puzzle:
    :param FinalSoln:
    :param tautology_switch:
    :param pure_switch:
    :param unit_switch: puts clauses of size one to true
    :return: FinalSoln, puzzle (puzzle only contains unsatisfied clauses)
    """

    stop_simplifying_check = 0
    is_inconsistent = 0
    while stop_simplifying_check == 0:   # stops when nothing has changed in the last simplification
        stop_simplifying_check = 1
        var_list = []   # for pure literal simplification
        for clause in puzzle:
            clause_remove_check = 0 # checks if the clause can be removed due to any of the simplification rules
            for var in clause:
                # tautology
                if tautology_switch == 1:
                    if -1 * var in clause:
                        clause_remove_check = 1
                        stop_simplifying_check = 0
                # unit clause
                if unit_switch == 1:
                    if len(clause) == 1 and FinalSoln[abs(var)] == 0:
                        if var < 0:
                            FinalSoln[abs(var)] = -1
                        else:
                            FinalSoln[var] = 1
                        clause_remove_check = 1
                        stop_simplifying_check = 0
                    if len(clause) == 1 and FinalSoln[abs(var)]*var > 0:
                        clause_remove_check = 1
                        stop_simplifying_check = 0
                    if len(clause) == 1 and FinalSoln[abs(var)]*var < 0:
                        is_inconsistent = 1
                        stop_simplifying_check = 1
                # pure
                if pure_switch == 1:
                    var_list.append(var)

            if clause_remove_check == 1:
                puzzle.remove(clause)

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
            for var in clause:
                if FinalSoln[abs(var)] != 0:
                    if FinalSoln[abs(var)]*var > 0: #remove satisfied clause
                        puzzle.remove(clause)
                        stop_simplifying_check = 0
                        break
                    else:   #romoves assigned variable form clause
                        clause.remove(var)
                        stop_simplifying_check = 0
            if len(clause) == 0:
                is_inconsistent = 1
                stop_simplifying_check = 1
                break

    return FinalSoln, puzzle, is_inconsistent

# ----------Splitting----------
def split(FinalSoln, puzzle, FinalSoln_history, puzzle_history, chosen_list, Heuristic, is_inconsistent):
    """
    gets the puzzle and solution and both their histories and the list of variables that were chosen for spiltting
    before. It checks for unassigned variables and adds them to vars_to_split. If there was no var to split, it
    back tracks. It looks for the closest var that has value 1 and switches that to -1; and reverts the puzzle and
    solution to their state before that var was splitted. If there are no splitted vars to turn into -1 and there are
    no unassigned vars, the puzzle is unsolvable.
    :param FinalSoln:
    :param puzzle:
    :param FinalSoln_history:
    :param puzzle_history:
    :param chosen_list: ordered list of all the variables that were splitted before
    :param Heuristic:
    :return:
    """
    # we can only split those that are not assigned yet
    vars_to_split = []
    for var in FinalSoln:
        if FinalSoln[var] == 0:
            vars_to_split.append(var)

    backtrack_to = 0    # backtrack_to =0: there is nothing to backtrack to, another variable is chosen in the same branch
    if is_inconsistent == 1: # no split options left, have to back track, or reached inconsistency
        for var in reversed(chosen_list):
            if FinalSoln[abs(var)] == 1:
                puzzle = puzzle_history[var]
                FinalSoln = FinalSoln_history[var]
                FinalSoln[var] = -1
                backtrack_to = var
                break
            chosen_list.remove(var)
        if len(chosen_list) == 0:
            print('the puzzle is inconsistent')
            backtrack_to = None

    if len(vars_to_split) != 0 and is_inconsistent == 0:
        if Heuristic == 'random':
            split_var = random.choice(vars_to_split)
        if Heuristic == 'JW_onesided':
            split_var = JW_onesided(puzzle, vars_to_split)
        if Heuristic == 'DLIS':
            split_var = DLIS(puzzle, vars_to_split, FinalSoln)
        puzzle_history[split_var] = deepcopy(puzzle)
        FinalSoln_history[split_var] = deepcopy(FinalSoln) #FinalSoln[:]
        FinalSoln[split_var] = 1
        chosen_list.append(split_var)



    return FinalSoln, puzzle, puzzle_history, FinalSoln_history, chosen_list, backtrack_to

# ----------Stopping----------
def stop(puzzle,FinalSoln):
    """
    checks if we should stop. If found_solution is 1, we have a solution. If it is 0, we don't.
    :param puzzle:
    :param FinalSoln:
    :return:
    """
    found_solution = 1
    for clause in puzzle:
        clause_sat = 0
        for var in clause:
            if FinalSoln[abs(var)]*var > 0:
                clause_sat = 1
        if clause_sat == 0:
            found_solution = 0
            break
    return found_solution
#add inconsistant


# ----------Main----------
def SAT(heuristic_switch, puzzle):
    """
    :param heuristic_switch:
    :param puzzle:
    :return:
    """
    # To initialize 'blank' soln
    chosen_list = []
    puzzle_history = {}
    FinalSoln_history = {}
    FinalSoln = {}

    for i in puzzle:
        for j in i:
            FinalSoln[abs(j)] = 0  # They are initialized as 0, true is 1 and false is -1

    if heuristic_switch == 1:
        Heuristic = 'random'
    elif heuristic_switch == 2:
        Heuristic = 'DLIS'
    elif heuristic_switch == 3:
        Heuristic = 'JW_onesided'
    else:
        raise ValueError('Invalid Heuristic Switch')

    tautology_switch = 1
    pure_switch = 0
    unit_switch = 1

    FinalSoln, puzzle, is_inconsistent = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
    stop_check = stop(puzzle, FinalSoln)

    tautology_switch = 0
    pure_switch = 0

    a=1
    while stop_check == 0:
        FinalSoln, puzzle, puzzle_history, FinalSoln_history, chosen_list, backtrack_to = split(FinalSoln,
                                                                                                puzzle, FinalSoln_history,
                                                                                                puzzle_history, chosen_list,
                                                                                                Heuristic,is_inconsistent)

        #print(chosen_list)

        FinalSoln, puzzle, is_inconsistent = simplify(puzzle, FinalSoln, tautology_switch, pure_switch, unit_switch)
        stop_check = stop(puzzle, FinalSoln)
        # if stop_check ==1:
        #     print(a)

        if backtrack_to is None:
            stop_check = 1

        # print('iter',a)
        a +=1
    return FinalSoln

# To initialize our problem
for i in range(1,50):
    myRulesList = readDIMACS('sudoku-rules.txt')
    puzzle = []

    start = time.time()
    myPuzzle = readDIMACS('top91.sdk.txt',i)
    puzzle = myRulesList + myPuzzle
    sol = SAT(2,puzzle)
    end = time.time()

    print(end - start)