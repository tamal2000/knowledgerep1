import json
import re

def processString(unprocessedString):
    sudokuID1 = int((re.search(r'\d*$', unprocessedString)).group(0))
    sudokuID2 = (re.search(r'.txt.\d*$', unprocessedString)).group(0)
    fileName = re.sub(sudokuID2,'', unprocessedString)+str('.txt')

    return fileName, sudokuID1


myFile, sudokuNum = processString("top91.sdk.txt1")

with open('metric_history.txt') as f:
    metric_history = json.load(f)
with open('time_history.txt') as f:
    time_history = json.load(f)

easy = {}
medium = {}
hard = {}
super_hard = {}
fileNames = ['top91.sdk.txt', '1000 sudokus.txt','damnhard.sdk.txt','subig20.sdk.txt','top95.sdk.txt','top100.sdk.txt','top870.sdk.txt','top2365.sdk.txt']
for name in fileNames:
    easy[name] = []
    medium[name] = []
    hard[name] = []
    super_hard[name] = []


for p in metric_history:
    myFile, sudokuNum = processString(p)
    if metric_history[p][0] == 0:
        easy[myFile].append(sudokuNum)
    elif metric_history[p][0]<10:
        medium[myFile].append(sudokuNum)
    elif metric_history[p][0]<100:
        hard[myFile].append(sudokuNum)
    else:
        super_hard[myFile].append(sudokuNum)

print(easy)
# with open('easy.txt', 'w') as file:
#      file.write(json.dumps(easy))
# with open('medium.txt', 'w') as file:
#     file.write(json.dumps(medium))
# with open('hard.txt', 'w') as file:
#     file.write(json.dumps(hard))
# with open('super_hard.txt', 'w') as file:
#     file.write(json.dumps(super_hard))