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
