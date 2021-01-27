import numpy as np
import pandas as pd
import sys
import math
from tabulate import tabulate

def isValidPrior(data):
    if (data.values < 0).any():
        return False
    elif data.sum(axis=1)[0] != 1.0:
        return False
    return True

def getPrior(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1)
    data = data.fillna(0.0)
    if isValidPrior(data):
        return data
    return None

def isValidChannel(data):
    if (data.values < 0).any():
        return False
    elif (data.sum(axis=1) != 1.0).any():
        return False
    return True

def getChannel(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=2)
    data = data.fillna(0.0)
    if isValidChannel(data):
        return data
    return None

def getN(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1, skiprows=1)
    data = data.fillna(0.0)
    return data

def calculateJoint(filename):
    prior = getPrior(filename)
    channel = getChannel(filename)
    if prior is None or channel is None:
        return
    prior = pd.DataFrame(np.tile(prior,(len(channel.columns),1)))
    joint = channel
    joint = joint * prior.T
    return joint

def calculateOuter(data):
    df = pd.DataFrame(data.sum())
    return df.T

def calculatePosterior(joint, py):
    py = 1.0 / py
    py = pd.DataFrame(np.tile(py,(len(joint.index),1)))
    posterior = joint * py
    return posterior

def calculateProbNTries(n, posterior, colID):
    numRows = n.iloc[0][0]
    end = len(posterior.columns)
    index = end - numRows

    ordered = posterior.T.sort_values(by=[colID])
    ordered.index = range(0, len(posterior.columns))
    ordered = ordered.iloc[index:]
    return ordered[colID].sum()

def calculateNTries(posterior, outer, n):
    ncols = len(posterior.columns)

    entropy = 0.0
    for i in range(0, ncols):
        pNTries = calculateProbNTries(n, posterior.T, i)
        entropy = entropy + (pNTries * outer[i])

    return entropy

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        joint = calculateJoint(sys.argv[1])
        outer = calculateOuter(joint)
        n = getN(sys.argv[1])
        posterior = calculatePosterior(joint, outer)
        entropy = calculateNTries(posterior, outer, n)
        
        print("Bayes Posterior Entropy")
        print(entropy.iloc[0])
        print('---------------------------')
    else:
        print("File not found")

main()
