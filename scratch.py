import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def reject_outliers(data, m=2): #
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def getMyData(fileName):
    """
    Processes the data saved in the dictionaries by removing all outliers, regrouping data by list index, and
    returning mean and standard deviation as two separate lists. (A format that is easy to plot.)

    :param fileName:
    :return: mean and standard deviation for a metric based on element indices
    """
    with open(fileName) as f:  # splits metrics
        myMetricsData = json.load(f)
    metricCountList = list(myMetricsData.values())
    # reoriganize lists so: index = number of vars removed listofList[index] = all data for puzzles when the have index number of variables
    metricCountList = np.stack(metricCountList, axis=1)
    # Processing data and extracting means and standard deviation for each variable popped
    metricMean = []
    metricStdev = []
    for listbyVarCount in metricCountList:
        listbyVarCount2 = reject_outliers(listbyVarCount)  # remove outliers
        # Get means for each list
        listMean = np.mean(listbyVarCount2)
        metricMean.append(listMean)
        # Get standard deviation for each list
        listStdev = np.std(listbyVarCount2)
        metricStdev.append(listStdev)
    return metricMean, metricStdev

# ----------------------- Code being developed ------------------------------------

dummyMeans1, dummyStdev1 = getMyData('time_history_popVars_SHard_backtrack.txt')
dummyMeans2, dummyStdev2 = getMyData('time_history_popVars_SHard.txt')
dummyMeans3, dummyStdev3 = getMyData('time_history_popVars_SHard.txt')
dummyMeans = [np.mean(dummyMeans1), np.mean(dummyMeans2), np.mean(dummyMeans3)]
dummyStdevs = [np.mean(dummyStdev1), np.mean(dummyStdev2), np.mean(dummyStdev3)]


heuristics = ('No Heuristics', 'Heuristic 1', 'Heuristic 2')
y_pos = np.arange(len(heuristics))

sns.set()
#plt.bar(y_pos, dummyMeans, align='center', alpha=0.8, color=('royalblue', 'maroon'))
plt.bar(y_pos, dummyMeans, yerr=dummyStdevs, align='center', alpha=0.9, color=('cornflowerblue', 'royalblue', 'navy'), ecolor='black', capsize=10)
plt.xticks(y_pos, heuristics)
plt.ylabel('$\Delta$ Splits',fontsize=18)

plt.show()
