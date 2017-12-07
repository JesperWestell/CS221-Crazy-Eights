import pickle
import evaluate
import numpy as np
from rl_agent import RLAgent
from game_rules import gameRules
import random
import math
from util import saveWeights,loadWeights
import util
from sklearn import linear_model
import collections

from crazy_eights_game import Observation, GameState, CardPile

opponent = 'OracleAgent'
numGames = 20
iterations = 10

def loadExamples(name):
    with open(name,'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            return []

def saveExamples(examples,name):
    with open(name,'wb') as f:
        pickle.dump(examples,f)

def rescale(x):
    if x==0: return 0
    return 100/(1+np.exp(-(2*x-1)*8))

def learnTransitionProbs(N=5):
    logs = evaluate.runGames(N, ['BasicMinimaxAgent', opponent], 2, isLogging=True)[1]
    valuable_logs = []
    # p(action|state) = p(action,state)/p(state)
    actionAndStateProb = collections.Counter()
    stateProb = collections.Counter()
    for log in logs:
        valuable_logs += [l[1:] for l in log if l[0] != 0]
    numExamples = len(valuable_logs)
    for l in valuable_logs:
        features = l[0]
        stateProb[tuple(features)] += 1./numExamples
        actionAndStateProb[tuple(features+util.actionFeatureExtractor(l[1]))] \
            +=1./numExamples

    actionAndStateProbList = []
    stateProbList = []

    for f in actionAndStateProb:
        actionAndStateProbList.append((f,actionAndStateProb[f]))
    for f in stateProb:
        stateProbList.append((f, stateProb[f]))

    saveExamples(actionAndStateProbList,'action_and_state_prob_new.txt')
    saveExamples(stateProbList,'state_prob_new.txt')

def generateRandomState():
    state = GameState(0,
                      gameRules.numStartingCards,
                      gameRules.suits,
                      gameRules.ranks,
                      gameRules.multiplicity,
                      2)
    newHands = []
    for hand in state.hands:
        newHand = CardPile()
        limit = random.uniform(0,1)
        for card in hand.pile:
            rand = random.uniform(0,1)
            if rand > limit:
                newHand.add(card)
        if newHand.isEmpty():
            newHand.add(state.deck.takeRandomly())
        newHands.append(newHand)
    state.hands = newHands

    newDeck = CardPile()
    limit = random.uniform(0, 1)
    for card in state.deck.pile:
        rand = random.uniform(0,1)
        if rand > limit and state.deck.size() > 1:
            n = int(math.ceil(random.uniform(0,1)*state.deck.look(card)))
            newDeck.add_n(card,n)
    state.deck = newDeck

    for i in range(len(state.numsTaken)):
        state.numsTaken[i] = random.randint(0,3)
    return state

def getExamples(n):
    examples = []
    for _ in range(n):
        print _+1
        state = generateRandomState()
        value = evaluate.runGames(numGames,['BasicMinimaxAgent',opponent],0,state)[0][0]
        examples.append((util.stateFeatureExtractor(Observation(0,state)),value))
    return examples

def createTrainingExamples(n):
    examples = getExamples(n)
    saveExamples(examples, 'rl_examples_new.txt')

def GD(name,weights_file):
    trainExamples = loadExamples(name)
    X = []
    Y = []
    for example in trainExamples:
        X.append(example[0])
        Y.append(example[1])
    X = np.array(X)
    Y = np.array(Y)

    model = linear_model.LinearRegression(fit_intercept=False)
    model.fit(X, Y)
    weights = list(model.coef_)
    print(weights)
    saveWeights(weights,weights_file)

def mergeExamples(name1,name2,output):
    examples1 = loadExamples(name1)
    examples2 = loadExamples(name2)
    saveExamples(examples1+examples2,output)
    create_exp_examples()

def create_exp_examples():
    trainExamples = loadExamples('rl_examples.txt')
    exp_examples = []
    mean = 0
    for e in trainExamples:
        mean += e[1]
    mean /= float(len(trainExamples))
    for e in trainExamples:
        #exp_examples.append((e[0],100*math.pow(1.3,e[1]-20)))
        exp_examples.append((e[0],rescale(e[1]/float(numGames))))
    saveExamples(exp_examples,'exp_examples.txt')


def main():
    #learnTransitionProbs(50000)
    #mergeExamples('action_and_state_prob.txt',
    #              'action_and_state_prob_new.txt',
    #              'action_and_state_prob.txt')
    #mergeExamples('state_prob.txt',
    #              'state_prob_new.txt',
    #              'state_prob.txt')
    #GD('action_and_state_prob.txt','action_and_state_weights.txt')
    #GD('state_prob.txt', 'state_weights.txt')

    #createTrainingExamples(485)
    #mergeExamples('rl_examples.txt','rl_examples_new.txt','rl_examples.txt')
    #print(len(loadExamples('rl_examples.txt')))

    #create_exp_examples()
    # use exp_examples.txt!!

    GD('exp_examples.txt', 'rl_weights.txt')

    #print(len(loadExamples('rl_examples2.txt')))
    #print len(loadExamples('rl_examples.txt'))
    #lst = loadExamples('rl_examples.txt')
    #saveWeights([-5.52586772e-01, 8.35091871e-01, 2.52975060e-02, 9.09851529e-03, 1.56949300e+01])
    #saveWeights([0.0 for i in range(5)])


if __name__ == '__main__':
    main()