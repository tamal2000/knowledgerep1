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
            line = list(map(int,line))
            line = line[0:len(line)-1] # removes zero from the end of each line
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
for i in rulesList:
    for j in i:
        FinalSoln[abs(j)] = 0



"""
# Appending given Sudoku puzzle to the list of rules so it's built in the problem we have
print(rulesList)


# Intializing soln representation as a dictionary
FinalSoln = {}
for i in rulesList:
    for j in i:
        FinalSoln[abs(j)] = 0
        """


