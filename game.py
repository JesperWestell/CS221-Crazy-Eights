from crazy_eights_game import CrazyEightsGame, Observation
from keyboard_agent import KeyboardAgent
from baseline_agent import BaselineAgent
from oracle import OracleAgent
from copy import copy
from game_rules import gameRules
from crazy_eights_game import Suit
import util


class Game:
    def __init__(self):
        self.startingIndex = 0
        self.agents = [OracleAgent(index=0), BaselineAgent(index=1)]
        self.numAgents = 2
        self.verbose = True

    def run(self):
        agentIndex = self.startingIndex
        CEG = CrazyEightsGame(startingPlayer=agentIndex,
                              numStartingCards=gameRules.numStartingCards,
                              suits=gameRules.suits,
                              ranks=gameRules.ranks,
                              multiplicity=gameRules.multiplicity)
        gameState = CEG.startState()

        #changed here, isEnd() as a function of gameState, not of CEG.
        while not gameState.isEnd():
            agent = self.agents[agentIndex]
            if self.verbose:
                print '\nAgent %s\'s turn' % agentIndex
            observation = Observation(agentIndex, gameState=copy(gameState))
            action = agent.getAction(observation)
            gameState = gameState.getSuccessor(action)
            if self.verbose:
                print('Agent %s performed action %s' % (agentIndex,action))
            agentIndex = (agentIndex + 1) % self.numAgents
        if self.verbose:
            print '\nGame over, agent %s won' % ((agentIndex - 1) % self.numAgents)

game = Game()
game.run()
