import pandas as pd
import sys
from tabulate import tabulate

def getChannel(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=1)
    data = data.fillna(0.0)
    return data

def printChannel(filename):
    prior = getChannel(filename)
    prior = prior.add_prefix("Ch(E_")
    prior = prior.add_suffix(")")
    print(prior.to_markdown())

def main():
    if len(sys.argv) == 2:
        print('--------- Output ----------')
        printChannel(sys.argv[1])
        print('---------------------------')
    else:
        print("File not found")

main()
