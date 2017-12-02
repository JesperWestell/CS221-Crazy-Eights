from itertools import combinations, chain
import sys
import inspect
import pickle
from game_rules import Suit, Actions

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

def loadWeights(name):
    with open(name,'rb') as f:
        return pickle.load(f)

def saveWeights(weights,name):
    with open(name,'wb') as f:
        pickle.dump(weights,f)

def actionFeatureExtractor(action):
    move = [(0, 1)[action[0] == Actions.PASS],
            (0, 1)[action[0] == Actions.TAKE]]
    rank = [0 for i in range(13)]
    suit = [0 for i in range(4)]
    if action[1] != None:
        card = action[1][0]
        rank[card.rank - 1] = 1
        suit = [(0, 1)[card.suit == Suit.HEART],
                (0, 1)[card.suit == Suit.DIAMOND],
                (0, 1)[card.suit == Suit.CLUB],
                (0, 1)[card.suit == Suit.SPADE]]
    return move+rank+suit

def stateFeatureExtractor(state):
    numberOfObserverCards = state.getHandSize()
    numberOfOpponentCards = sum(state.handsizes) - \
                            state.getHandSize()
    numberOfObserverEights = sum([state.getHand().look(card) for card
                                  in state.getHand().pile if
                                  card.rank == 8])
    numberOfDeckCards = state.getDeckSize()
    numberOfSameRank = sum(1 for card in state.getHand().pile
                           if card.rank == state.cardOnTable.rank)
    numberOfSameSuit = sum(1 for card in state.getHand().pile
                           if card.suit == state.cardOnTable.suit)

    return [numberOfObserverCards,
            numberOfOpponentCards,
            numberOfObserverEights,
            numberOfDeckCards,
            numberOfSameRank,
            numberOfSameSuit,
            1]


def dot(weights, features):
    assert len(features) == len(weights)
    return sum([w * f for w, f in zip(weights, features)])