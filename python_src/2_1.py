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
    print("PRIOR (REPEATED):")
    print(prior.to_markdown())
    print("CHANNEL:")
    print(channel.to_markdown())
    print("JOINT:")
    print(joint.to_markdown())

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        calculateJoint(sys.argv[1])
        print('---------------------------')
    else:
        print("File not found")

main()
