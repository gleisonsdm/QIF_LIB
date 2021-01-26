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

def calculateGuessingEntropy(data):
    data = data.T.sort_values(by=[0], ascending=False).T
    n = len(data.columns)
    entropy = 0.0
    for i in range(0,n):
        entropy = entropy + ((i+1) * data.T.iloc[i][0])
    return entropy

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        prior = getPrior(sys.argv[1])
        entropy = calculateGuessingEntropy(prior)
        print("GUESSING ENTROPY")
        print(entropy)
        print('---------------------------')
    else:
        print("File not found")

main()
