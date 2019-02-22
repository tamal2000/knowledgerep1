import json
a =[1,2,2,3,None]
try:
    a.remove(4)
except:
    pass
print(a.count(2))

b ={}
b['a',1] = [1]
b['a',1].append(3)

with open('metric_history.txt') as f:
    myBenchmarks = json.load(f)
print(myBenchmarks)