from itertools import combinations, chain
import sys
import inspect
import pickle
import numpy as np

def getCombinations(lst):
    combs = []
    for length in range(1,len(lst)+1):
        subsets = list(combinations(lst, length))
        for i, v in enumerate(subsets):
            subsets[i] = list(v)
        combs += subsets
    return combs

def raiseNotDefined():
  print("Method not implemented: %s" % inspect.stack()[1][3])
  sys.exit(1)

def loadWeights():
    with open('rl_weights.txt','rb') as f:
        return pickle.load(f)

def saveWeights(weights):
    with open('rl_weights.txt','wb') as f:
        pickle.dump(weights,f)