from crazy_eights_game import CrazyEightsGame, Observation
from keyboard_agent import KeyboardAgent
from baseline_agent import BaselineAgent
from oracle import OracleAgent
from minimax_agent import MinimaxAgent
from copy import copy
import game_rules
from crazy_eights_game import Suit
import util


class Game:
    def __init__(self,
                 gameRules = game_rules.ClassicGameRules,
                 agents = [OracleAgent(index=0), BaselineAgent(index=1)],
                 verbose = True):
        self.gameRules = gameRules
        self.startingIndex = 0
        self.agents = agents
        self.numAgents = len(agents)
        self.verbose = verbose

    def run(self):
        agentIndex = self.startingIndex
        CEG = CrazyEightsGame(startingPlayer=agentIndex,
                              numStartingCards=self.gameRules.numStartingCards,
                              suits=self.gameRules.suits,
                              ranks=self.gameRules.ranks,
                              multiplicity=self.gameRules.multiplicity,
                              numPlayers=self.numAgents)
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
        winner = (agentIndex - 1) % self.numAgents
        if self.verbose:
            print '\nGame over, agent %s won' % winner
        return winner

