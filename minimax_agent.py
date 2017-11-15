from agent import Agent
import random

class MinimaxAgent(Agent):
    """
    A minimax agent.
    """

    def __init__(self, index=0, depth = '4'):
        self.index = index
        self.keys = []

        #added a depth and a evaluation function.
        self.depth = int(depth)

    def getAction(self, state):
        actions =  state.getLegalActions()


        def recurse(state, depth, agentIndex, alpha, beta):

            choices = []

            if state.isEnd():
                return state.Utility()

            if depth == 0:
                return self.evaluationFunction(state)

            # if is the other agent, tries to minimize
            if agentIndex == (self.index+1)%2:
                for action in state.getLegalActions():
                    choices.append(recurse(state.getSuccessor(action), depth-1, 0, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)

            if agentIndex == self.index:
                for action in state.getLegalActions():
                    choices.append(recurse(state.getSuccessor(action), depth, 1, alpha, beta))
                    if alpha >= beta:
                        break
                    if min(choices) > alpha:
                        alpha = min(choices)
                return max(choices)


        values = [(recurse(state.getSuccesor(action), self.depth, (self.index+1)%2,float('-inf'), float('+inf')) for action in state.getLegalActions())]
        value = max(values)

        #chose a random action from one of the bests.
        bestIndices = [index for index in range(len(values)) if values[index] == value]
        chosenIndex = random.choice(bestIndices)

        return values[chosenIndex]


    def evaluationFunction(self, currentState):

        numberOfCards = currentState.hands[self.index]

        optimalScore = numberOfCards

        return optimalScore



