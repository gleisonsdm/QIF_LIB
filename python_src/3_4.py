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

def getN(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1)
    data = data.fillna(0.0)
    return data

def getPrior(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=[0], nrows=2)
    data = data.fillna(0.0)
    if isValidPrior(data):
        return data
    return None

def calculateProbNTries(n, prior):
    numRows = n.iloc[0][0]
    end = len(prior.columns)
    index = end - numRows

    ordered = prior.T.sort_values(by=[0])
    ordered = ordered.iloc[index:]
    return ordered.sum()

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        prior = getPrior(sys.argv[1])
        n = getN(sys.argv[1])
        entropy = calculateProbNTries(n, prior)
        print("PROBABILITE in N TRIES")
        print(entropy.to_markdown())
        print('---------------------------')
    else:
        print("File not found")

main()
