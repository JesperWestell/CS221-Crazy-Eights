from agent import Agent
import random

class BasicMinimaxAgent(Agent):
    """
    A minimax agent.
    """

    def __init__(self, index=0, depth = 1):
        self.index = index
        self.keys = []

        #added a depth and a evaluation function.
        self.depth = int(depth)

    def getAction(self, state):

        def recurse(state, depth, agentIndex, alpha, beta):
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
                    choices.append(recurse(state.getSuccessor(action), depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if min(choices) > alpha:
                        alpha = min(choices)
                return max(choices)
            elif agentIndex != state.numPlayers-1:
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action), depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)
            else:
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action), depth-1, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)


        actions = state.getLegalActions()
        values = [recurse(state.getSuccessor(action), self.depth, (self.index+1)%2,float('-inf'), float('+inf')) \
                   for action in actions]
        value = max(values)
        #chose a random action from one of the bests.
        bestIndices = [index for index in range(len(values)) if values[index] == value]
        chosenIndex = random.choice(bestIndices)
        best = actions[chosenIndex]
        return best


    def evaluationFunction(self, currentState):

        numberOfCards = currentState.getHandSize()

        optimalScore = -numberOfCards

        return optimalScore



