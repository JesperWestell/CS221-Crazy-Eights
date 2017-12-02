from agent import Agent
from crazy_eights_game import Actions, Card
from game_rules import gameRules

class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """

    def __init__(self, index=0):
        self.index = index
        self.keys = []

    def getAction(self, state):
        print('Card on table: %s' % state.getCardOnTable())
        print('Cards in hand: %s' % ['%s : %s' % (card, state.getHand().pile[card]) for
                                   card in state.getHand().pile])
        print('Number of cards in opponents hand: %s' % state.handsizes[(self.index+1)%2])
        while True:
            print('legal actions: %s ' % ['%s' % a + (' ' + ' '.join([ '%s %s' % (card.rank, card.suit) for card in cards])
                                                       if cards != None else '') for a,cards in state.getLegalActions()])
            x = raw_input('Make action: ').split()
            inputAction = x[0]
            inputCards = x[1:]
            cards = []
            if inputAction.lower() in Actions.AllActions:
                valid = True
                for rank,suit in zip(inputCards[::2],inputCards[1::2]):
                    valid, rank, suit = self.isValidCard(rank,suit)
                    if valid:
                        cards.append(Card(rank,suit))
                    else:
                        print('Wrong input format!')
                        break
                if not valid: continue
                if cards == []: cards = None
                for action in state.getLegalActions():
                    if self.compare((inputAction,cards),action):
                        return action
                print('Wrong input format!')
                continue
            else:
                print('Wrong input format!')

    def compare(self, action1, action2):

        a1, cs1 = action1
        a2, cs2 = action2
        if a1 == a2:
            if cs1 == None or cs2 == None:
                if a1 in [Actions.TAKE, Actions.PASS]:
                    return True
                else:
                    return False
            if len(cs1) != len(cs2):
                return False
            for card1, card2 in zip(cs1, cs2):
                if card1.suit != card2.suit or \
                                card1.rank != card2.rank:
                    return False
            return True

    def isValidCard(self, rank, suit):
        rank = int(rank)
        if rank not in gameRules.ranks:
            return False, None, None
        suit = suit.lower()
        if suit not in gameRules.suits:
            suit = suit[:-1]
            if suit not in gameRules.suits:
                return False, None, None
        return True, rank, suit
