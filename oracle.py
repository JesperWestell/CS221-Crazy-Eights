from agent import Agent
from crazy_eights_game import Card

class OracleAgent(Agent):
    """
    Oracle agent
    """

    def __init__(self, index=0):
        self.index = index
        self.keys = []

    def getAction(self, state):
        actions = state.getLegalActions()
        hand = self.createHand(state.getHand())
        stack_card = state.getCardOnTable()
        draw_count = state.getNumsTaken()

        decision = self.make_move(hand,stack_card,draw_count,'')
        if decision == 'draw' and ('take',None) in actions:
            return ('take',None)
        elif ('play',[decision]) in actions:
            return ('play',[decision])
        else:
            return ('pass', None)

    def createHand(self,cards):
        hand = []
        for card in cards.pile.keys():
            for i in range(cards.look(card)):
                hand.append(card)
        return hand

    # AI algorythm
    def make_move(self, hand, stack_card, draw_count, twisted_suit):
        # check if a smart twist can be made, if so twist
        for card in hand:
            if card.rank == stack_card.rank:
                suitcount = {}
                for card_ in hand:  # count suits
                    suitcount.setdefault(card_.suit, 0)
                    if not card_.rank == "8":  # don't count eights
                        suitcount[card_.suit] += 1
                try:
                    if suitcount[card.suit] > suitcount[stack_card.suit]:
                        return card
                except KeyError:
                    pass

        # check if suit, rank or eight in hand and play
        for card in hand:  # check if suit in hand
            if (
                    card.suit == stack_card.suit or card.suit == twisted_suit) and card.rank != "8":
                return card
        for card in hand:  # check if rank in hand
            if card.rank == stack_card.rank:
                return card
        for card in hand:  # check if eight in hand
            if card.rank == "8":
                suitcount = {}
                for card_ in hand:  # count suits
                    suitcount.setdefault(card_.suit, 0)
                    if not card_.rank == "8":  # don't count eights
                        suitcount[card_.suit] += 1

                newsuit = max(suitcount, key=suitcount.get)  # select plentiest suit
                return card, newsuit
        else:
            if draw_count < 3:
                return "draw"
            return "pass"