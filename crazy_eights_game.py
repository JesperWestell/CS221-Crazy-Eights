import random, collections
import util
from copy import copy
# TEST

class Suit:
    SPADE = 'spade'
    HEART = 'heart'
    CLUB = 'club'
    DIAMOND = 'diamond'

class Actions:
    PASS = 'pass'
    TAKE = 'take'
    PLAY = 'play'
    AllActions = [PASS,TAKE,PLAY]

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return '%s of %ss' % (self.rank,self.suit)

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __eq__(self, card2):
        if type(card2) == str:
            return False
        return self.suit == card2.suit and self.rank == card2.rank

class CardPile:
    def __init__(self):
        self.pile = collections.defaultdict(int)

    def look(self, card):
        return self.pile[card]

    def add_n(self, card, n):
        self.pile[card] += n

    def add(self, card):
        self.pile[card] += 1

    def remove(self, card):
        strcard = str(card)
        self.pile[card] -= 1
        assert self.pile[card] >= 0, 'card to remove was not in pile'
        if self.pile[card] == 0:
            del self.pile[card]

    def takeRandomly(self):
        card = random.choice(self.pile.keys())
        self.remove(card)
        return card

    def isEmpty(self):
        return not bool(self.pile)

    def size(self):
        size = 0
        for k in self.pile.keys():
            size += self.pile[k]
        return size

class GameState:
    def __init__(self, startingPlayer,
                 numStartingCards,
                 suits,
                 ranks,
                 multiplicity
                 ):

        self.numPlayers = 2
        self.numStartingCards = numStartingCards
        self.suits = suits
        self.ranks = ranks
        self.multiplicity = multiplicity
        self.deck = self.initializeDeck(suits, ranks, multiplicity)
        self.hands = self.initializeHands()
        self.player = startingPlayer
        self.cardOnTable = self.initializeCardOnTable()
        self.numsTaken = [0,] * self.numPlayers

    def initializeDeck(self, suits, ranks, multiplicity):
        deck = CardPile()
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                deck.add_n(card, multiplicity)
        return deck


    def initializeHands(self):
        hands =  []
        for p in range(self.numPlayers):
            hand = CardPile()
            for i in range(self.numStartingCards):
                card = self.deck.takeRandomly()
                hand.add(card)
            hands.append(hand)
        return hands

    def initializeCardOnTable(self):
        card = self.deck.takeRandomly()
        return card

    def isEnd(self):
        for hand in self.hands:
            if hand.isEmpty():
                return True
        return False

    def getLegalActions(self):
        """
        :param gameState: current game state
        :return: a list of actions that can be taken from the given game state
                each action will be in the form (action, cards) where:
                action - in {'take','play','pass'}
                cards - list of cards the player will play, in the correct order
        """
        actions = []
        actions.append((Actions.PASS, None))
        if self.numsTaken[self.player] < 3 and bool(self.deck.pile):
            actions.append((Actions.TAKE,None))
        for card in self.hands[self.player].pile.keys():
            if self.cardOnTable.suit == card.suit or \
                self.cardOnTable.rank == card.rank or \
                card.rank == 8:
                actions.append((Actions.PLAY, [card]))
                cardsWithSameRank = [c for c in self.hands[self.player].pile.keys()
                       if c.rank == card.rank and c != card]
                allCombinations = util.getCombinations(cardsWithSameRank)
                for c in allCombinations:
                    actions.append((Actions.PLAY,[card] + c))
        return actions

    def getSuccessor(self, newAction):
        newGameState = copy(self)
        action, cards = newAction
        if action == Actions.TAKE:
            newGameState.numsTaken[self.player] += 1
            newGameState.hands[self.player].add(newGameState.deck.takeRandomly())
        else:
            newGameState.numsTaken[self.player] = 0
            if action == Actions.PLAY:
                for card in cards:
                    newGameState.hands[self.player].remove(card)
                newGameState.cardOnTable = cards[-1]
        newGameState.player = (newGameState.player + 1) % 2
        if newGameState.deck.isEmpty():
            newGameState.deck = self.reshuffleDeck()
        return newGameState

    def reshuffleDeck(self):
        deck = self.initializeDeck(self.suits, self.ranks, self.multiplicity)
        for hand in self.hands:
            for card in hand.pile.keys():
                for i in range(hand.look(card)):
                    deck.remove(card)
        deck.remove(self.cardOnTable)
        return deck

class CrazyEightsGame:
    def __init__(self, numStartingCards = 6,
                 suits = [Suit.HEART,Suit.DIAMOND,Suit.CLUB,Suit.SPADE],
                 ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13],
                 multiplicity = 1,
                 startingPlayer = 0):
        """
        startingPlayer: index of player starting the game
        numStartingCards: integer representing number of cards each player will
        start with
        suits: subset of [HEART, DIAMOND, SPADE, CLUB], representing the suits
        used in the deck
        ranks: subset of [1,2,3,4,5,6,7,8,9,10,11,12,13], representing the ranks
        used in the deck. 8 will always be in game.
        multiplicity: integer representing the number of decks used
        """
        self.suits = suits
        self.ranks = set(ranks)
        self.ranks.add(8)
        self.multiplicity = multiplicity
        self.player = startingPlayer
        self.numStartingCards = numStartingCards
        self.startingPlayer = startingPlayer

    def startState(self):
        return GameState(self.startingPlayer,
                          self.numStartingCards,
                          self.suits,
                          self.ranks,
                          self.multiplicity
                         )

    def Player(self, gameState):
        return gameState.player

    def Utility(self, gameState):
        for i,hand in gameState.hands:
            if hand.isEmpty():
                return float('inf') if i == 0 else -float('inf')
