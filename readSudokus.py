import json
import random
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

# ---------------------To get all puzzles with x numbers of variables as a dictionary----------------------------------

def findSudokuByVarNum(filename, varNum=17):

    """
    :param filename: Sudoku file name that you wanted to search
    :param varNum: The numbers of variables that you're searching for. (Default value is 17).
    :return: List of puzzleID of all puzzles that satisfies varNum condition
    """

    # Opens file and automatically calculates the total number of Sudoku puzzles that the file contains
    with open(filename, "r") as myfile:
        fileText = myfile.read()
    fileText = fileText.replace("\n", "")
    totPuzzleNum = int(len(fileText) / 81)


    # Look through readDIMACS() of entire file
    SavedPuzzleIDs = []
    for i in range(0, totPuzzleNum):
        myPuzzle = readDIMACS(filename, i)
        if len(myPuzzle) == varNum:
            SavedPuzzleIDs.append(i)

    return SavedPuzzleIDs

def createMyBenchmarks(fileNamesList, desiredVarNum):
    """
    Call the function findSudokuByVarNum( ) for each file passed, and converts the output from that function into
    text file containing a dictionary. This function is meant to only run once.

    :param fileNamesList: list of file names
    :param desiredVarNum: how many variables you want your Sudoku puzzle to contain
    :return: 0
    """
    # Building a dictionary for all puzzles of X-variables long as {fileFoundIn: [sudokuPuzzleIDs]}
    benchmarkSudokos = {}
    for myFile in fileNamesList:
        # I chose 24 as a test, since both test files I have had 24 variable-long puzzles. Change back to 17 if you want to.
        foundSudokuMatches = findSudokuByVarNum(myFile, desiredVarNum)
        benchmarkSudokos[myFile] = foundSudokuMatches

    # Writing dictionary to hard drive as a text file
    with open('benchmarks.txt', 'w') as file:
        file.write(json.dumps(benchmarkSudokos))

    return 0

fileNames = ['top91.sdk.txt', '1000_sudokus.txt']
# Only run the line below ONCE. (Otherwise, you're just overwriting the results for the same file.)
createMyBenchmarks(fileNames, 24)

# How to open the text file as a dictionary
with open('benchmarks.txt') as f:
    myBenchmarks = json.load(f)
print(myBenchmarks)

# ---------------------------Write a function that randomly delete one variable from DIMACS lines----------------------
""" This wasn't worth rewriting as a function. It's just two lines of code. I figured you could just
incorporate into the main body of code."""

# Test puzzle to make sure it works
myPuzzle = readDIMACS('1000 sudokus.txt', 0)
# Make a deep copy, otherwise you'll be modifying the original puzzle!
NewPuzzle = deepcopy(myPuzzle)

# Line of code that randomly removes element from, and the test to see if list is an element shorter.
print(len(NewPuzzle))
NewPuzzle.pop(random.randrange(len(NewPuzzle)))
print(len(NewPuzzle))



