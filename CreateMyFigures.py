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

def makeScatterplot(dataDict, myXLabel, myYLabel): #Pass hard and easy puzzles IN THAT order

    fileNamesList = dataDict.keys()
    sns.set()
    myColors = ['royalblue', 'mediumvioletred']
    for index, myFile in enumerate(fileNamesList):
        meanMetric, stDevmetric = getMyData(myFile)
        xAxisRange = len(meanMetric) + 1
        # xAxis = list(range(1, xAxisRange))
        # make data frame to pass code into seaborn
        df = pd.DataFrame({'x': (range(1, xAxisRange)), 'y': meanMetric})
        plt.errorbar(df.index + 1, meanMetric, yerr=stDevmetric, fmt='-o', color=myColors[index],
                     label=dataDict[myFile])
    plt.xlabel(myXLabel, fontsize=18)
    plt.ylabel(myYLabel, fontsize=18)
    plt.legend()
    plt.show()

    return 0

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

# #-------------------------------- Plots for Pop Vars ----------------------------------------------------------
# dataSetPopsVarsHard_Splits = {'metric_history_popVars_splits_SHard.txt':'Super Hard Puzzles', 'metric_history_popVar_splits_Ceasy.txt': 'Easy Puzzles'}
# makeScatterplot(dataSetPopsVarsHard_Splits, 'Variables Removed', 'Splits Made')
#
#
# dataSetPopsVarsHard_Backtrack = {'metric_history_popVars_backtracks_SHard.txt':'Super Hard Puzzles', 'metric_history_popVar_backtracks_Ceasy.txt': 'Easy Puzzles'}
# makeScatterplot(dataSetPopsVarsHard_Backtrack, 'Variables Removed', 'Backtracks Made')
#
# # --------------------------------Plots for Multi-Solutions----------------------------------
# dataSet50Solns_Splits = {'metric_history_50sols_splits_SHard.txt':'Super Hard Puzzles', 'metric_history_50sols_splits_Ceasy.txt': 'Easy Puzzles'}
# makeScatterplot(dataSet50Solns_Splits, 'Solutions Found', 'Splits Made')
#
# dataSet50Solns_Backtracks = {'metric_history_50sols_backtracks_SHard.txt':'Super Hard Puzzles', 'metric_history_50sols_backtracks_Ceasy.txt': 'Easy Puzzles'}
# makeScatterplot(dataSet50Solns_Backtracks, 'Solutions Found', 'Backtracks Made')


##----------------------------------------- Histogram for heuristics ----------------------------------------------
# Cleaning and processing data
randomMeans = barPlotPrep('metric_history_DLIS_backtracks_SHard.txt')
dummyMeans = barPlotPrep('metric_history_DLIS_backtracks_Ceasy.txt')
DLSIMeans = barPlotPrep('metric_history_DLIS_backtracks_Ceasy.txt')
# Aggregating Data
heuristicMeans = [np.mean(randomMeans), np.mean(dummyMeans), np.mean(DLSIMeans)]
heuristicStdev = [np.std(randomMeans), np.std(dummyMeans), np.std(DLSIMeans)]

# plotting data
heuristics = ('No Heuristics', 'One-Sided JW Heuristic', 'DSLI Heuristic')
y_pos = np.arange(len(heuristics))
sns.set()
plt.bar(y_pos, heuristicMeans, yerr=heuristicStdev , align='center', alpha=0.9, color=('cornflowerblue', 'royalblue', 'navy'), ecolor='black', capsize=10)
plt.xticks(y_pos, heuristics)
plt.ylabel('Splits Made',fontsize=18)
plt.show()