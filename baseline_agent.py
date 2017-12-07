from agent import Agent
import random

class BaselineAgent(Agent):
    """
    A simple baseline agent, choosing actions randomly.
    """

    def __init__(self, index=0):
        self.index = index
        self.keys = []

    def getAction(self, state):
        actions = state.getLegalActions()
        if len(actions) > 1:
            actions = [a for a in actions if a != ('take', None)]
        return random.choice(actions)
