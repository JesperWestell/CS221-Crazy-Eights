from agent import Agent
import random
import util

class QLPruneAgent(Agent):
    """
    Q-learning agent, learning by exploring and exploiting.
    """

    def __init__(self, index=0, learning = False):
        self.index = index
        self.keys = []
        self.learning = learning
        self.epsilon = 0.8
        self.discount = 0.7
        self.alpha = 1.0
        #a dictionary for saving the best values of each (state, action) key
        self.Qvalues = {}
        self.counter = 0


    def getAction(self, state):
        actions = state.getLegalActions()

        if not self.learning:
            return random.choice(actions)

        if self.learning:
            self.counter += 1
            action = self.chooseAction(state)
            # I save the tuple (s, a, r, s') for learning.
            successor = state.getSuccessor(action)
            reward = successor.Utility()
            #if successor.isEnd() == True:
            #    print reward
            self.learn(state, action, reward, successor)
            return action


    def chooseAction(self, state):
        #self.checkStateInValues(state)
        if random.random() < self.epsilon:
            return random.choice(state.getLegalActions())
        else:
            # see if any actions have been learned.
            learned = False
            for action in state.getLegalActions():
                if (self.realState(state), self.realAction(action)) in self.Qvalues.keys():
                    learned = True

            maxValue = 0.0
            bestAction = ''
            if learned == True:
                for action in state.getLegalActions():
                    value = self.Qvalues[(self.realState(state), self.realAction(action))]
                    if value >= maxValue:
                        maxValue, bestAction = value, action
                return bestAction
            else:
                return random.choice(state.getLegalActions())


    def learn(self, s, a, r, succ):
        #check if maxQ if succ is different than zero, and if reward is different than zero. Save (prunning if not)
        learning = False
        if r != 0:
            print 'Im in end state'
            learning = True
        for newAction in succ.getLegalActions():
            #print 'successor action that could happen', newAction
            print 'keys!!!!!', self.Qvalues.keys()
            print 'successor state, action', (self.realState(succ), self.realAction(newAction))
            #print 'successor action', self.realAction(newAction)
            if (self.realState(succ), self.realAction(newAction)) in self.Qvalues.keys():
                print 'IM making progress!!'
                learning = True
        if learning == True:
            #ensure all the actions of that state are saved in Qtable, not only the action chosen.
            for act in s.getLegalActions():
                if (self.realState(s), self.realAction(act) not in self.Qvalues.keys()):
                    self.Qvalues[(self.realState(s), self.realAction(act))] = 0.0
                    #print 'newAction', act
                    #print 'newValues', self.Qvalues

            prediction = self.Qvalues[(self.realState(s), self.realAction(a))]
            if succ.isEnd() == True:
                target = r
            else:
                print "IM in maxQSucc"
                print self.realState(succ)
                maxQSucc = max([self.Qvalues[(self.realState(succ), self.realAction(action))] for action in succ.getLegalActions()])
                target = r + self.discount*maxQSucc
            self.Qvalues[(self.realState(s), self.realAction(a))] += self.alpha*(target - prediction)

    def realAction(self, action):
        if action[0] == 'play':
            return (action[0], tuple(action[1]))
        else:
            return action

    def realState(self, state):
        myList = util.stateFeatureExtractor(state)
        myList = myList + state.hand.pile.keys()
        #myList.append(state.hand)
        return tuple(myList)
        #return (state.observer, state.player, tuple(state.suits), tuple(state.ranks), state.hand, state.deckSize)
