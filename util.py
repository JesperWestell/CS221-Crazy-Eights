from itertools import combinations, chain
import sys
import inspect
import pickle
from game_rules import Suit, Actions, ClassicGameRules

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
    card_features = []
    for suit in Suit.all:
        for rank in range(1,13+1):
            card_features.append(
                sum(state.unknowns.look(card) for card in state.unknowns.pile
                    if card.suit == suit and card.rank == rank))


    return [numberOfObserverCards,
            numberOfOpponentCards,
            numberOfObserverEights,
            numberOfDeckCards,
            numberOfSameRank,
            numberOfSameSuit,
            1] + card_features

def dot(weights, features):
    assert len(features) == len(weights)
    return sum([w * f for w, f in zip(weights, features)])


def getdrawProbabilities(state):
    suits = ClassicGameRules.suits
    ranks = ClassicGameRules.ranks
    drawProbSuits = {key: 0 for key in suits}
    drawProbRanks = {key: 0 for key in ranks}
    # Count remaining cards in unknowns and return probabilities of each card d
    #print(
    #'Cards in RLhand: %s' % ['%s : %s' % (card, state.getHand().pile[card]) for
    #                         card in state.getHand().pile])

    #print(
    #'Cards in deck: %s' % ['%s : %s' % (card, state.getUnknowns().pile[card])
    #                       for
    #                       card in state.getUnknowns().pile])
    suits = [card.suit for card in state.getUnknowns().pile]
    ranks = [card.rank for card in state.getUnknowns().pile]

    for suit in suits:
        drawProbSuits[suit] += 1

    for rank in ranks:
        drawProbRanks[rank] += 1

    unknowns_base = float(len(suits))

    drawProbSuits = {k: v / unknowns_base for k, v in drawProbSuits.iteritems()}
    drawProbRanks = {k: v / unknowns_base for k, v in drawProbRanks.iteritems()}

    return drawProbSuits, drawProbRanks


def getLearnedTransProbabilities(state, action):
    state_weights = \
        loadWeights('state_weights.txt')
    action_and_state_weights = \
        loadWeights('action_and_state_weights.txt')
    state_features = stateFeatureExtractor(state)
    action_features = actionFeatureExtractor(action)

    state_prob = dot(state_weights, state_features)
    action_and_state_prob = dot(action_and_state_weights,
                                     state_features + action_features)
    action_given_state_prob = action_and_state_prob / state_prob
    return action_given_state_prob