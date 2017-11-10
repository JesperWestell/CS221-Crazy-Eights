from crazy_eights_game import CrazyEightsGame
from keyboard_agent import KeyboardAgent
from baseline_agent import BaselineAgent
from copy import copy
from game_rules import gameRules
from crazy_eights_game import Suit
import util

class Observation:
    def __init__(self,agentIndex,gameState):
        self.hand = gameState.hands[agentIndex]
        self.cardOnTable = gameState.cardOnTable
        self.numsTaken = gameState.numsTaken[agentIndex]
        self.isEmptyDeck = gameState.deck.isEmpty()
        self.legalActions = gameState.getLegalActions()

    def getHand(self):
        return self.hand
    def getCardOnTable(self):
        return self.cardOnTable
    def getNumsTaken(self):
        return self.numsTaken
    def isEmptyDeck(self):
        return self.isEmptyDeck
    def getLegalActions(self):
        return self.legalActions

class Game:
    def __init__(self):
        self.startingIndex = 0
        self.agents = [KeyboardAgent(), BaselineAgent()]
        self.numAgents = 2
        self.verbose = True

    def run(self):
        agentIndex = self.startingIndex
        CEG = CrazyEightsGame(startingPlayer=agentIndex)
        gameState = CEG.startState()

        #changed here, isEnd() as a function of gameState, not of CEG.
        while not gameState.isEnd():
            agent = self.agents[agentIndex]
            if self.verbose:
                print '\nAgent %s\'s turn' % agentIndex
            observation = Observation(agentIndex, copy(gameState))
            action = agent.getAction(observation)
            gameState = gameState.getSuccessor(action)
            if self.verbose:
                print('Agent %s performed action %s' % (agentIndex,action))
            agentIndex = (agentIndex + 1) % self.numAgents
        if self.verbose:
            print '\nGame over, agent %s won' % ((agentIndex - 1) % self.numAgents)

game = Game()
game.run()
