import random, collections
import game_rules
from game_rules import Suit
import util
import copy

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
        self.pile = collections.Counter()

    def __add__(self, other):
        new = CardPile()
        new.pile = copy.copy(self.pile)
        new.pile += other.pile
        return new

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
        if self.pile[card] <= 0:
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
    '''
    GameState for Crazy Eights Card Game
    '''
    def __init__(self, startingPlayer,
                 numStartingCards,
                 suits,
                 ranks,
                 multiplicity,
                 numPlayers
                 ):

        self.numPlayers = numPlayers
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
        hands = []
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

        cardOnTable = self.cardOnTable
        hand = self.hands[self.player]
        numsTaken = self.numsTaken[self.player]
        deckSize = self.deck.size()
        return getLegalActions(cardOnTable, hand, numsTaken, deckSize)

    def getSuccessor(self, newAction):
        newGameState = copy.deepcopy(self)
        action, cards = newAction
        if action == Actions.TAKE:
            newGameState.numsTaken[self.player] += 1
            card = newGameState.deck.takeRandomly()
            newGameState.hands[self.player].add(card)
            if newGameState.deck.isEmpty():
                newGameState.deck = self.reshuffleDeck()
                newGameState.deck.remove(card)
        else:
            newGameState.numsTaken[self.player] = 0
            if action == Actions.PLAY:
                for card in cards:
                    newGameState.hands[self.player].remove(card)
                newGameState.cardOnTable = cards[-1]
            if newGameState.deck.isEmpty():
                newGameState.deck = self.reshuffleDeck()
        newGameState.player = (newGameState.player + 1) % self.numPlayers
        return newGameState

    def reshuffleDeck(self):
        deck = self.initializeDeck(self.suits, self.ranks, self.multiplicity)
        for hand in self.hands:
            for card in hand.pile:
                for i in range(hand.look(card)):
                    deck.remove(card)
        deck.remove(self.cardOnTable)
        return deck

    def Utility(self):
        for i,hand in self.hands:
            if hand.isEmpty():
                return float('inf') if i == 0 else -float('inf')

class Observation:
    '''
        Observation will serve as a 'fake' version of GameState, with the same
        functions, but without the real values of the deck and opponents hand
        Objects of this class will be used by agents when deciding on the best
        action to make
    '''
    def __init__(self, agentIndex, gameState):
        self.observer = agentIndex
        self.player = agentIndex
        self.suits = gameState.suits
        self.ranks = gameState.ranks
        self.multiplicity = gameState.multiplicity
        self.hand = gameState.hands[self.observer]
        self.handsizes = [hand.size() for hand in gameState.hands]
        self.cardOnTable = gameState.cardOnTable
        self.numsTaken = copy.copy(gameState.numsTaken)
        self.legalActions = gameState.getLegalActions()
        self.deckSize = gameState.deck.size()
        self.unknowns = gameState.deck
        self.numPlayers = gameState.numPlayers
        for i in range(len(gameState.hands)):
            if i != self.observer:
                self.unknowns += gameState.hands[i]

    def getSuits(self):
        return self.suits

    def getHandSize(self):
        return self.handsizes[self.player]

    def getRanks(self):
        return self.ranks

    def getMultiplicity(self):
        return self.multiplicity

    def getHand(self):
        return self.hand

    def getCardOnTable(self):
        return self.cardOnTable

    def getNumsTaken(self):
        return self.numsTaken[self.player]

    def isEmptyDeck(self):
        return self.getDeckSize() == 0

    def getDeckSize(self):
        return self.deckSize

    def getLegalActions(self):
        cardOnTable = self.getCardOnTable()
        hand = self.getHand() if self.player == self.observer else self.unknowns
        numsTaken = self.getNumsTaken()
        deckSize = self.getDeckSize()
        return getLegalActions(cardOnTable, hand, numsTaken, deckSize)

    def getSuccessor(self,newAction):
        newObservation = copy.deepcopy(self)
        action, cards = newAction
        if action == Actions.TAKE:
            newObservation.numsTaken[self.player] += 1
            newObservation.handsizes[self.player] += 1
            newObservation.deckSize -= 1
        else:
            newObservation.numsTaken[self.player] = 0
            if action == Actions.PLAY:
                for card in cards:
                    newObservation.handsizes[self.player] -= 1
                    if self.observer != self.player:
                        newObservation.unknowns.remove(card)
                newObservation.cardOnTable = cards[-1]
        newObservation.player = (newObservation.player + 1) % len(self.handsizes) # Number of players
        if newObservation.isEmptyDeck():
            self.reshuffleDeck()
        return newObservation

    def reshuffleDeck(self):
        self.deckSize = len(self.getSuits())*len(self.getRanks())*self.getMultiplicity() \
        - sum(handSize for handSize in self.handsizes) - 1

    def isEnd(self):
        for size in self.handsizes:
            if size == 0:
                return True
        return False

    def Utility(self):
        for i,hand in enumerate(self.handsizes):
            if hand == 0:
                return float('inf') if i == self.observer else -float('inf')
        return 0

def getLegalActions(cardOnTable, hand, numsTaken, deckSize):
    actions = []
    actions.append((Actions.PASS, None))
    if numsTaken < 3 and deckSize > 0:
        actions.append((Actions.TAKE, None))
    for card in hand.pile.keys():
        if cardOnTable.suit == card.suit or \
                        cardOnTable.rank == card.rank or \
                        card.rank == 8:
            actions.append((Actions.PLAY, [card]))
            if game_rules.CHAIN_RULE:
                cardsWithSameRank = [c for c in hand.pile.keys()
                                 if c.rank == card.rank and c != card]
                allCombinations = util.getCombinations(cardsWithSameRank)
                for c in allCombinations:
                    actions.append((Actions.PLAY, [card] + c))
    return actions

class CrazyEightsGame:
    def __init__(self, numStartingCards = 6,
                 suits = [Suit.HEART,Suit.DIAMOND,Suit.CLUB,Suit.SPADE],
                 ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13],
                 multiplicity = 1,
                 startingPlayer = 0,
                 numPlayers = 2):
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
        self.numPlayers = numPlayers

    def startState(self):
        return GameState(self.startingPlayer,
                          self.numStartingCards,
                          self.suits,
                          self.ranks,
                          self.multiplicity,
                          self.numPlayers)

    def Player(self, gameState):
        return gameState.player
