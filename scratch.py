# Saving rules as a list to be referenced later
rulesList = []
f = open("sudoku-rules.txt", "r")
for line in f:
    line = line.split()
    # Use 'try' and 'except' to skip over any non-integer lists
    try:
        line = list(map(int,line))
        line = line[0:len(line)-1] # removes zero from the end of each line
        rulesList.append(line)
    except:
        pass


# Appending given Sudoku puzzle to the list of rules so it's built in the problem we have
print(rulesList)


# Intializing soln representation as a dictionary
FinalSoln = {}
for i in rulesList:
    for j in i:
        FinalSoln[abs(j)] = 0