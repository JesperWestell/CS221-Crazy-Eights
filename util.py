from itertools import combinations, chain
import sys
import inspect

def getCombinations(lst):
    combs = []
    for length in range(1,len(lst)+1):
        subsets = list(combinations(lst, length))
        for i, v in enumerate(subsets):
            subsets[i] = list(v)
        combs += subsets
    return combs

def raiseNotDefined():
  print "Method not implemented: %s" % inspect.stack()[1][3]
  sys.exit(1)