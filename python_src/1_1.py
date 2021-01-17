import pandas as pd
import sys

def main():
    if len(sys.argv) == 2:
        data = pd.read_csv(sys.argv[1], delimiter=";", header=None)
        data = data.fillna(0.0)
        print("--------------------")
        if (data.values < 0).any():
            print("Invalid Values")
        elif data.sum(axis=1)[0] != 1.0:
            print("Values are not a probabilistic distribution")
        else:
            print("Values are a probabilistic distribution")
    else:
        print("File not found")

main()
