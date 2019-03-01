import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def reject_outliers(data, m=2):  #
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


def barPlotPrep(fileName):
    with open(fileName) as f:  # splits metrics
        myMetricsData = json.load(f)
    metricList = list(myMetricsData.values())
    flatMetricList = []
    for singleList in metricList:
        for listElement in singleList:
            flatMetricList.append(listElement)

    print(flatMetricList)
    flatMetricList2 = np.asarray(flatMetricList)
    flatMetricList2 = reject_outliers(flatMetricList2, 0.5)

    return flatMetricList2


meanSplitsforVarsRemovedHard, stDevforVarsRemovedHard = getMyData('metric_history_popVars_splits_SHard.txt')
meanSplitsforVarsRemovedEasy, stDevforVarsRemovedEasy = getMyData('metric_history_popVar_splits_Ceasy.txt')

xAxisRange = len(meanSplitsforVarsRemovedHard) + 1
xAxis = list(range(1,xAxisRange))
# make data fram to pass code into seaborn
df = pd.DataFrame({'x': (range(1,xAxisRange)), 'y': meanSplitsforVarsRemovedHard})
# plot
sns.set()
plt.errorbar(df.index+1, meanSplitsforVarsRemovedHard, yerr=stDevforVarsRemovedHard, fmt='-o', color = 'royalblue', label='Super Hard Puzzles')
#placeholder for easy puzzles
plt.errorbar(df.index, meanSplitsforVarsRemovedEasy, yerr=stDevforVarsRemovedEasy, fmt='-x', color='mediumvioletred', label='Easy Puzzles')
plt.xlabel('Variables Removed', fontsize=18)
plt.ylabel('Splits Made',fontsize=18)
plt.legend()
plt.show()