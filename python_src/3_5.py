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

def getGainFunction(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=1)
    data = data.fillna(0.0)
    return data

def getPrior(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1)
    data = data.fillna(0.0)
    if isValidPrior(data):
        return data
    return None

def calculateGVulnerability(gfunc, prior):
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

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        prior = getPrior(sys.argv[1])
        gfunc = getGainFunction(sys.argv[1])
        gvuln = calculateGVulnerability(gfunc, prior)
        print("G Vulnerability")
        print(gvuln)
        print('---------------------------')
    else:
        print("File not found")

main()
