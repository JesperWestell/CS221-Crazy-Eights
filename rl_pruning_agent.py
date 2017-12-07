from agent import Agent
import random
import util

class RLPruningAgent(Agent):
    """
    A mix of RL and pruning agent.
    """

    def __init__(self, index=0, depth = 1):
        self.index = index
        self.numActionsToPick = 5
        self.keys = []

        #added a depth and a evaluation function.
        self.depth = int(depth)

    def getAction(self, state):
        def recurse(state, depth, agentIndex, alpha, beta):
            assert state.player == agentIndex
            choices = []
            nextAgentIndex = (agentIndex + 1) % state.numPlayers
            if state.isEnd():
                return state.Utility()
            if depth == 0:
                return self.evaluationFunction(state)
            # if is the other agent, tries to minimize
            if agentIndex == self.index:
                actions = state.getLegalActions()
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action), depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if min(choices) > alpha:
                        alpha = min(choices)
                return max(choices)
            elif agentIndex != state.numPlayers-1:
                actions = self.maximizeProbActions(state, self.numActionsToPick)
                for action in actions:
                    choices.append(recurse(state.getSuccessor(action), depth, nextAgentIndex, alpha, beta))
                    if alpha >= beta:
                        break
                    if max(choices) < beta:
                        beta = max(choices)
                return min(choices)
            else:
                actions = self.maximizeProbActions(state, self.numActionsToPick)
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

    def maximizeProbActions(self,state,N):
        actions = state.getLegalActions()
        actionProbs = []
        for a in actions:
            actionProbs.append(util.getLearnedTransProbabilities(state,a))
        prioList=[x for _, x in sorted(zip(actionProbs, actions),
                                           key=lambda pair: -pair[0])]
        return prioList[:N]

    def evaluationFunction(self, currentState):
        features = util.stateFeatureExtractor(currentState)
        optimalScore = util.dot(util.loadWeights('rl_weights.txt'),features)
        return optimalScore



