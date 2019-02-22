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

# ---------------------------To get all puzzles with x numbers of variables -------------------------------------------
# TODO Convert this code into function with inputs: (filename , VarNum)
# TODO Function needs to return: (filename, sudokuIDsList)
# myPuzzle = readDIMACS('top91.sdk.txt', 0)
filename = 'top91.sdk.txt'

# Opens file and automatically calculates the total number of Sudoku puzzles that the file contains
with open(filename, "r") as myfile:
    fileText = myfile.read()
fileText = fileText.replace("\n", "")
totPuzzleNum = int(len(fileText) / 81)
print(totPuzzleNum )
# Look through readDIMACS() of entire file
SavedPuzzleIDs = []
for i in range(0, totPuzzleNum):
    myPuzzle = readDIMACS('top91.sdk.txt', i)
    if len(myPuzzle) == 17:
        SavedPuzzleIDs.append(i)
print(SavedPuzzleIDs)

# TODO once complete function, find a way to build filename, sudokuIDsList into dictionary of {filename : sudokuIDsList}
# TODO save output as a dictionary file onto hard drive and check that it can be read




# ---------------------------Write a function that randomly delete one variable from DIMACS lines----------------------

