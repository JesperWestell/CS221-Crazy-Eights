from agent import Agent
import random
import util

class RLProbAgent(Agent):
    """
    An RLProb agent.
    """

    def __init__(self, index=0, depth = 1):
        self.index = index
        self.keys = []

        #added a depth and a evaluation function.
        self.depth = int(depth)

    def getAction(self, state):
        # cards = self.getdrawProbabilties(state)
        def recurse(state, maxDepth, depth, agentIndex, alpha, beta):
            choices = []
            actions = state.getLegalActions()
            nextAgentIndex = (agentIndex + 1) % state.numPlayers
            if state.isEnd():
                return state.Utility()
            if depth == 0:
                return self.evaluationFunction(state)
            # if is the other agent, tries to minimize
            if agentIndex == self.index:
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action),maxDepth, depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if min(choices) > alpha:
                        alpha = min(choices)
                if depth == maxDepth:
                    return actions[choices.index(max(choices))]
                else:
                    return max(choices)
            elif agentIndex != state.numPlayers-1:
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action),maxDepth, depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)
            else:
                #print('Len actions: {0}'.format(len(actions)))
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action),maxDepth, depth-1, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)

        action = recurse(state,self.depth,self.depth,self.index,float('-inf'), float('+inf'))
        return action

    def getFeatures(self, currentState):
        numberOfObserverCards = currentState.getHandSize()
        numberOfOpponentCards = sum(currentState.handsizes) - \
                                currentState.getHandSize()
        numberOfObserverEights = sum([currentState.getHand().look(card) for card
                                      in currentState.getHand().pile if
                                      card.rank == 8])
        numberOfDeckCards = currentState.getDeckSize()

        return [numberOfObserverCards,
                numberOfOpponentCards,
                numberOfObserverEights,
                numberOfDeckCards,
                1]

    def evaluate(self,features):
        weights = util.loadWeights()
        return sum([w*f for w,f in zip(weights,features)])

    def evaluationFunction(self, currentState):
        features = self.getFeatures(currentState)
        optimalScore = self.evaluate(features)
        return optimalScore



