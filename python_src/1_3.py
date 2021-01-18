import pandas as pd
import sys
from tabulate import tabulate

def getPrior(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1)
    data = data.fillna(0.0)
    return data

def printPrior(filename):
    prior = getPrior(filename)
    prior = prior.add_prefix("P(E_")
    prior = prior.add_suffix(")")
    print(prior.to_markdown())

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        printPrior(sys.argv[1])
        print('---------------------------')
    else:
        print("File not found")

main()
