import numpy as np
import pandas as pd
import sys
from tabulate import tabulate

def isValidPrior(data):
    if (data.values < 0).any():
        return False
    elif data.sum(axis=1)[0] != 1.0:
        return False
    return True

def isValidChannel(data):
    if (data.values < 0).any():
        return False
    elif (data.sum(axis=1) != 1.0).any():
        return False
    return True

def calculateJoint(filename):
    prior = getPrior(filename)
    channel = getChannel(filename)
    if prior is None or channel is None:
        return
    prior = pd.DataFrame(np.tile(prior,(len(channel.columns),1)))
    joint = channel
    joint = joint * prior.T
    return joint

def calculatePY(data):
    df = pd.DataFrame(data.sum())
    print("P(x|Y)")
    print(df.T)
    return df.T

def calculatePosterior(joint, py):
    py = 1.0 / py
    print("COEF")
    print(py)
    py = pd.DataFrame(np.tile(py,(len(joint.index),1)))
    posterior = joint * py
    return posterior

def calculateHyperMatrix(data):
    toDrop = []
    indexes = range(1,(len(data.columns)+1))
    titles = [("y" + str(i)) for i in indexes]
    visited = {}
    for t in indexes:
        visited[t] = False

    for name, values in data.iteritems():
        for i in range((int(name)+1),len(data.columns)):
            comparison = np.where(data[name] == data[i], 1, 0).sum()
            if visited[i] == True:
                continue
            if comparison == len(data.index):
                titles[name] = titles[name] + " or " + titles[i]
                toDrop.append(titles[i])
                visited[i] = True

    data.columns = titles    
    data = data.drop(toDrop, axis=1)
    data.add_prefix('P(X|')
    data.add_suffix(')')
    return data

def calculateShannonEntropyPrior(data):
    logs = data.apply(lambda x: x * math.log(x))
    logs = (logs.T.sum() * -1)
    return logs

def calculateGuessingEntropyPrior(data):
    data = data.T.sort_values(by=[0], ascending=False).T
    n = len(data.columns)
    entropy = 0.0
    for i in range(0,n):
        entropy = entropy + ((i+1) * data.T.iloc[i][0])
    return entropy

def calculateBayesVulnerabilityPrior(data):
    return data.T.max()

def calculateProbNTriesPrior(n, prior):
    numRows = n.iloc[0][0]
    end = len(prior.columns)
    index = end - numRows

    ordered = prior.T.sort_values(by=[0])
    ordered = ordered.iloc[index:]
    return ordered.sum()

def calculateGVulnerabilityPrior(gfunc, prior):
    ncols = len(prior.columns)
    nrows = len(gfunc.index)

    maxim = 0.0
    for i in range(0, nrows):
        value = 0.0
        for j in range(0,ncols):
            value = value + gfunc.iloc[i, j] * prior.iloc[0, j]
        if maxim < value:
            maxim = value

    return maxim

def calculateOuter(data):
    df = pd.DataFrame(data.sum())
    return df.T

def applyShannon(val):
    if val == 0.0:
        return 0.0
    return val * math.log(val)

def calculateShannonEntropyPosterior(data, outer):
    logs = data.applymap(applyShannon)
    logs = logs.sum()
    entropy = logs * outer
    entropy = (entropy.T.sum() * -1)
    return entropy

def calculateGuessingEntropyByColumn(data, index):
    data = data.sort_values(by=[index], ascending=False)
    data.index = range(0,len(data.index))
    n = len(data.index)
    entropy = 0.0
    for i in range(0,n):
        entropy = entropy + ((i+1) * data.T.iloc[index][i])
    return entropy

def calculateGuessingEntropyPosterior(data, outer):
    ncols = len(data.columns)
    nrwos = len(data.index)
 
    entropy = 0.0
    for i in range(0,ncols):
        guessing = calculateGuessingEntropyByColumn(data, i)
        entropy = entropy + (guessing * outer[i])

    return entropy

def calculateBayesEntropyPosterior(data, outer):
    ncols = len(data.columns)
    nrwos = len(data.index)
 
    entropy = 0.0
    for i in range(0,ncols):
        bayes = data.T.iloc[i].max()
        entropy = entropy + (bayes * outer[i])

    return entropy

def calculateProbNTries(n, posterior, colID):
    numRows = n.iloc[0][0]
    end = len(posterior.columns)
    index = end - numRows

    ordered = posterior.T.sort_values(by=[colID])
    ordered.index = range(0, len(posterior.columns))
    ordered = ordered.iloc[index:]
    return ordered[colID].sum()

def calculateNTriesPosterior(posterior, outer, n):
    ncols = len(posterior.columns)

    entropy = 0.0
    for i in range(0, ncols):
        pNTries = calculateProbNTries(n, posterior.T, i)
        entropy = entropy + (pNTries * outer[i])

    return entropy

def calculateGVulnerabilityPosterior(posterior, outer, gainFunc):
    nColPost = len(posterior.columns)
    nRowPost = len(posterior.index)
    nColGain = len(gainFunc.columns)
    nColOuter = len(outer.columns)
    
    vulnerability = 0.0
    for i in range(0, nColPost):
        best = 0.0
        for k in range(0, nColGain):
            vuln = 0.0
            for j in range(0, nRowPost):
                vuln = vuln + posterior.iloc[j, i] * gainFunc.iloc[k, j]
            if vuln > best:
                best = vuln
        vulnerability = vulnerability + best * outer.iloc[0, i]

    return vulnerability

def calculateAdditiveLeakage(Gvprior, Gvpost):
    leak = Gvpost - Gvprior
    return leak

def calculateMultiplicativeLeakage(Gvprior, Gvpost):
    if Gvprior == 0.0:
        return 99999999.99999999
    leak = Gvpost / Gvprior
    return leak

