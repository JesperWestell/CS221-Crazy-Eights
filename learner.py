import pickle
import evaluate
import numpy as np
from rl_agent import RLAgent
from game_rules import gameRules
import random
import math
from util import saveWeights,loadWeights
from sklearn import linear_model

from crazy_eights_game import Observation, GameState, CardPile

opponent = 'OracleAgent'
numGames = 20
iterations = 10

def loadExamples(name):
    with open(name,'rb') as f:
        return pickle.load(f)

def saveExamples(examples,name):
    with open(name,'wb') as f:
        pickle.dump(examples,f)

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
    agent = RLAgent()
    for _ in range(n):
        print _+1
        state = generateRandomState()
        value = evaluate.runGames(numGames,['BasicMinimaxAgent',opponent],0,state)[0]
        examples.append((agent.getFeatures(Observation(0,state)),value))
    return examples

def createTrainingExamples(n):
    examples = getExamples(n)
    saveExamples(examples, 'rl_examples_new.txt')

def GD(name):
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
    print(model.coef_)
    saveWeights(list(model.coef_))

def mergeExamples(name1,name2,output):
    examples1 = loadExamples(name1)
    examples2 = loadExamples(name2)
    saveExamples(examples1+examples2,output)

def create_exp_examples():
    trainExamples = loadExamples('rl_examples.txt')
    exp_examples = []
    for e in trainExamples:
        exp_examples.append((e[0],100*math.pow(1.2,e[1]-20)))
        print exp_examples[-1][1]
    saveExamples(exp_examples,'exp_examples.txt')

def main():
    createTrainingExamples(500)
    #GD('rl_examples_added_features.txt')
    #create_exp_examples()
    #saveWeights([0.0 for i in range(5)])
    mergeExamples('rl_examples_added_features.txt','rl_examples_new.txt','rl_examples_added_features.txt')
    #print len(loadExamples('rl_examples.txt'))
    #lst = loadExamples('rl_examples.txt')
    #saveWeights([-5.52586772e-01, 8.35091871e-01, 2.52975060e-02, 9.09851529e-03, 1.56949300e+01])
    #saveWeights([0.0 for i in range(5)])


if __name__ == '__main__':
    main()