import json

with open('metric_history.txt') as f:
    metric_history = json.load(f)
with open('time_history.txt') as f:
    time_history = json.load(f)

easy = {}
medium = {}
hard = {}
super_hard = {}
for p in metric_history:
    if metric_history[p][0] == 0:
        easy[p] = metric_history[p]
    elif metric_history[p][0]<10:
        medium[p] = metric_history[p]
    elif metric_history[p][0]<100:
        hard[p] = metric_history[p]
    else:
        super_hard[p] = metric_history[p]

with open('easy.txt', 'w') as file:
     file.write(json.dumps(easy))
with open('medium.txt', 'w') as file:
    file.write(json.dumps(medium))
with open('hard.txt', 'w') as file:
    file.write(json.dumps(hard))
with open('super_hard.txt', 'w') as file:
    file.write(json.dumps(super_hard))