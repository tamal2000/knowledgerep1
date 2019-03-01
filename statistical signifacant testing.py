import json
from statistics import mean
from copy import deepcopy
import random



def significance_testing(file_easy,file_hard,number_of_tests,alpha):
    #loading results
    with open(file_easy) as f:
        easy = json.load(f)
    with open(file_hard) as f:
        hard = json.load(f)

    # making two lists with the metrics
    easy_vals = []
    for puzzle in easy:
        for val in easy[puzzle]:
            easy_vals.append(int(val))

    hard_vals = []
    for puzzle in hard:
        for val in hard[puzzle]:
            hard_vals.append(int(val))

    #find the initial average of difference
    delta = [h-e for h, e in zip(hard_vals, easy_vals)]
    initial_avg = mean(delta)

    avgs = []
    for i in range(number_of_tests):
        copy_easy_vals = deepcopy(easy_vals)
        copy_hard_vals = deepcopy(hard_vals)

        if len(copy_easy_vals) != len(copy_hard_vals):
            raise ValueError('lengths are not equal')

        #select a random position and swap
        index = random.choice(range(0,len(easy_vals)))
        temp = hard_vals [index]
        hard_vals [index] = easy_vals [index]
        easy_vals [index] = temp

        #calculate average
        delta = [h - e for h, e in zip(hard_vals, easy_vals)]
        avgs.append(mean(delta))

        #swapping back
        easy_vals = copy_easy_vals
        hard_vals = copy_hard_vals

    #sorting the averages
    avgs.append(initial_avg)
    avgs.sort()
    index = avgs.index(initial_avg)
    if index >= (1-alpha)*len(avgs):
        print('The difference is NOT statistically significant.')
        result = 0
    else:
        print('The difference IS statistically significant.')
        result = 1
    return result

ST_popVars_backtrack = significance_testing('metric_history_popVar_backtracks_Ceasy.txt','metric_history_popVars_bracktracks_SHard.txt',100,0.05)
ST_popVars_split = significance_testing('metric_history_popVar_splits_Ceasy.txt','metric_history_popVars_splits_SHard.txt',100,0.05)

ST_50sols_backtrack = significance_testing('metric_history_50sols_backtracks_Ceasy.txt','metric_history_50sols_backtracks_SHard.txt',100,0.05)
ST_50sols_split = significance_testing('metric_history_50sols_splits_Ceasy.txt','metric_history_50sols_splits_SHard.txt',100,0.05)

print('popVar splits:', ST_popVars_split)
print('popVar backtracks:', ST_popVars_backtrack)
print('popVar splits:', ST_50sols_split)
print('popVar backtracks:', ST_50sols_backtrack)
