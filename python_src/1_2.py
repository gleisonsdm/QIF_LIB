import pandas as pd
import sys

def isValid(data):
    if (data.values < 0).any():
        return False
    elif (data.sum(axis=1) != 1.0).any():
        return False
    return True

def main():
    if len(sys.argv) == 2:
        data = pd.read_csv(sys.argv[1], delimiter=";", header=None)
        data = data.fillna(0.0)
        print("--------------------")
        if isValid(data):
            print("Valid")
        else:
            print("Invalid")
    else:
        print("File not found")

main()
