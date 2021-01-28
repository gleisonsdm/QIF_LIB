import numpy as np
import pandas as pd
import sys
import math
from tabulate import tabulate
from numpy import *

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

def getChannel(filename, chanSize):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=chanSize, skiprows=2)
    data = data.fillna(0.0)
    if isValidChannel(data):
        return data
    return None

def getChannelSize(filename):
    data = pd.read_csv(filename, delimiter=";", header=None, nrows=1, skiprows=1)
    data = data.fillna(0.0)
    return data.iloc[0][0]

def getGainFunction(filename, chanSize):
    toSkip = chanSize + 2
    data = pd.read_csv(filename, delimiter=";", header=None, skiprows=toSkip)
    data = data.fillna(0.0)
    return data

def calculateJoint(prior, channel):
    if prior is None or channel is None:
        return
    prior = pd.DataFrame(np.tile(prior,(len(channel.columns),1)))
    joint = channel
    joint = joint * prior.T
    return joint

def calculateOuter(data):
    df = pd.DataFrame(data.sum())
    return df.T

def calculatePosterior(joint, py):
    py = 1.0 / py
    py = pd.DataFrame(np.tile(py,(len(joint.index),1)))
    posterior = joint * py
    return posterior

def calculateGVulnerabilityPrior(gfunc, prior):
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

def calculateGVulnerabilityPosterior(posterior, outer, gainFunc):
    nColPost = len(posterior.columns)
    nRowPost = len(posterior.index)
    nColGain = len(gainFunc.columns)
    nColOuter = len(outer.columns)
    
    vulnerability = 0.0
    for i in range(0, nColPost):
        best = 0.0
        for k in range(0, nColGain):
            vuln = 0.0
            for j in range(0, nRowPost):
                vuln = vuln + posterior.iloc[j, i] * gainFunc.iloc[k, j]
            if vuln > best:
                best = vuln
        vulnerability = vulnerability + best * outer.iloc[0, i]

    return vulnerability

def calculateAdditiveLeakage(Gvprior, Gvpost):
    leak = Gvpost - Gvprior
    return leak

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print('--------- Output ----------')
        prior = getPrior(filename)
        chanSize = getChannelSize(filename)
        channel = getChannel(filename, chanSize)

        joint = calculateJoint(prior, channel)
        outer = calculateOuter(joint)
        gainF = getGainFunction(filename, chanSize)

        posterior = calculatePosterior(joint, outer)
      
        priVul = calculateGVulnerabilityPrior(gainF, prior)
        postVul = calculateGVulnerabilityPosterior(posterior, outer, gainF)
        
        vulnerability = calculateAdditiveLeakage(priVul, postVul)

        print("G-Vulnerability Additive Leakage")
        print(vulnerability)
        print('---------------------------')
    else:
        print("File not found")

main()
