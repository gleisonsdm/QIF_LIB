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

def calculateBayesVulnerability(data):
    return data.T.max()

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        prior = getPrior(sys.argv[1])
        entropy = calculateBayesVulnerability(prior)
        print("BAYES ENTROPY")
        print(entropy.to_markdown())
        print('---------------------------')
    else:
        print("File not found")

main()
