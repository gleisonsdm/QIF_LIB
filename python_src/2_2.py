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

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        joint = calculateJoint(sys.argv[1])
        py = calculatePY(joint)
        posterior = calculatePosterior(joint, py)
        reduced = calculateHyperMatrix(posterior)
        print("HYPER")
        print(reduced.to_markdown())
        print('---------------------------')
    else:
        print("File not found")

main()
