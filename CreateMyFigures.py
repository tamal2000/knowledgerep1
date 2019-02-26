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

def makeScatterPlot(meansList, standardDev): # Use it or delete it
    for index, singlemeansList in enumerate(meansList):
        xAxisRange = len(singlemeansList) + 1
        xAxis = list(range(1, xAxisRange))
        # making dataframe to pass to seaborn
        df = pd.DataFrame({'x': (range(1, xAxisRange)), 'y': meansList})
        # plotting
        sns.set()
        plt.errorbar(df.index + 1, meansList, yerr=standardDev[index], fmt='-o')

    plt.xlabel('Variables Removed', fontsize=18)
    plt.ylabel('Number of Splits', fontsize=18)
    plt.show()
    return 0

# -------------------------------- Plots for Pop Vars ----------------------------------------------------------
meanSplitsforVarsRemoved, stDevforVarsRemoved = getMyData('metric_history_popVars_SHard.txt')

xAxisRange = len(meanSplitsforVarsRemoved) + 1
xAxis = list(range(1,xAxisRange))
# make data fram to pass code into seaborn
df = pd.DataFrame({'x': (range(1,xAxisRange)), 'y': meanSplitsforVarsRemoved})
# plot
sns.set()
plt.errorbar(df.index+1, meanSplitsforVarsRemoved, yerr=stDevforVarsRemoved, fmt='-o', color = 'royalblue', label='Super Hard Puzzles')
#placeholder for easy puzzles
#plt.errorbar(df.index, meanSplitsforVarsRemoved, yerr=stDevforVarsRemoved, fmt='-x', color='mediumvioletred', label='Easy Puzzles')
plt.xlabel('Variables Removed', fontsize=18)
plt.ylabel('Number of Splits',fontsize=18)
plt.legend()
plt.show()



# --------------------------- Plots for Multi-Solutions ------------------------------------------------------------
# For delta metric
meanSplitsforMultiSoln, _ = getMyData('metric_history_100sols_splits_SHard.txt')
meanSplitsforMultiSoln = np.diff(meanSplitsforMultiSoln)
stDevforMultiSoln = np.std(meanSplitsforMultiSoln)
xAxisRange = len(meanSplitsforMultiSoln) + 1
xAxis = list(range(1,xAxisRange))
# make data fram to pass code into seaborn
df = pd.DataFrame({'x': (range(1,xAxisRange)), 'y': meanSplitsforMultiSoln})
# plot
sns.set()
plt.errorbar(df.index+1, meanSplitsforMultiSoln, yerr=stDevforMultiSoln, fmt='-o', color = 'royalblue', label='Super Hard Puzzles')
#placeholder for easy puzzles
#plt.errorbar(df.index, meanSplitsforVarsRemoved, yerr=stDevforVarsRemoved, fmt='-x', color='mediumvioletred', label='Easy Puzzles')
plt.xlabel('Number of Solutions Found', fontsize=18)
plt.ylabel('Difference in Splits Made',fontsize=18)
plt.legend()
plt.show()


# for regular metric
meanSplitsforMultiSoln, stDevforMultiSoln = getMyData('metric_history_100sols_splits_SHard.txt')
xAxisRange = len(meanSplitsforMultiSoln) + 1
xAxis = list(range(1,xAxisRange))
# make data fram to pass code into seaborn
df = pd.DataFrame({'x': (range(1,xAxisRange)), 'y': meanSplitsforMultiSoln})
# plot
sns.set()
plt.errorbar(df.index+1, meanSplitsforMultiSoln, yerr=stDevforMultiSoln, fmt='-o', color = 'royalblue', label='Super Hard Puzzles')
#placeholder for easy puzzles
#plt.errorbar(df.index, meanSplitsforVarsRemoved, yerr=stDevforVarsRemoved, fmt='-x', color='mediumvioletred', label='Easy Puzzles')
plt.xlabel('Number of Solutions Found', fontsize=18)
plt.ylabel('Difference in Splits Made',fontsize=18)
plt.legend()
plt.show()


# ----------------------- Histogram for heuristics ------------------------------------

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
plt.ylabel('Number of Splits Made',fontsize=18)
plt.show()