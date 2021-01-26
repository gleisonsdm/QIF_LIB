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
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=1)
    data = data.fillna(0.0)
    if isValidChannel(data):
        return data
    return None

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

def applyShannon(val):
    if val == 0.0:
        return 0.0
    return val * math.log(val)

def calculateShannonEntropy(data, outer):
    logs = data.applymap(applyShannon)
    logs = logs.sum()
    entropy = logs * outer
    entropy = (entropy.T.sum() * -1)
    return entropy

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        joint = calculateJoint(sys.argv[1])
        outer = calculateOuter(joint)
        posterior = calculatePosterior(joint, outer)
        entropy = calculateShannonEntropy(posterior, outer)
        
        print("Shannon Posterior Entropy")
        print(entropy.to_markdown())
        print('---------------------------')
    else:
        print("File not found")

main()
