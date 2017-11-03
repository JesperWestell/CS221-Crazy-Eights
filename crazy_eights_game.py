import random, collections
import util
from copy import copy

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

    def __gt__(self, card2):
        return self.suit == card2.suit and self.rank == card2.rank

class CardPile:
    def __init__(self):
        self.pile = collections.defaultdict(int)

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

class GameState:
    def __init__(self, startingPlayer,
                 numStartingCards,
                 suits,
                 ranks,
                 multiplicity):
        self.numPlayers = 2
        self.numStartingCards = numStartingCards
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
        return newGameState

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
                          self.multiplicity)

    def Player(self, gameState):
        return gameState.player

    def isEnd(self, gameState):
        for hand in gameState.hands:
            if hand.isEmpty():
                return True
        return False

    def Utility(self, gameState):
        for i,hand in gameState.hands:
            if hand.isEmpty():
                return float('inf') if i == 0 else -float('inf')


game = CrazyEightsGame(20,[Suit.HEART,Suit.DIAMOND],[1,2,3,4,5,6,7,8],4)
gameState = game.startState()
actions = gameState.getLegalActions()
gameState.getSuccessor(actions[0])


"""
state = GameState(0,5,[Suit.HEART,Suit.DIAMOND],[1,2,3,4,5,6,7,8],1)
print state.cards
print state.deck
print state.hands
print state.cardOnTable
"""


"""

class Game:

  def __init__( self, agents, display, rules, startingIndex=0, muteAgents=False, catchExceptions=False ):
    self.agentCrashed = False
    self.agents = agents
    self.display = display
    self.rules = rules
    self.startingIndex = startingIndex
    self.gameOver = False
    self.muteAgents = muteAgents
    self.catchExceptions = catchExceptions
    self.moveHistory = []
    self.totalAgentTimes = [0 for agent in agents]
    self.totalAgentTimeWarnings = [0 for agent in agents]
    self.agentTimeout = False

  def getProgress(self):
    if self.gameOver:
      return 1.0
    else:
      return self.rules.getProgress(self)

  def _agentCrash( self, agentIndex, quiet=False):
    "Helper method for handling agent crashes"
    if not quiet: traceback.print_exc()
    self.gameOver = True
    self.agentCrashed = True
    self.rules.agentCrash(self, agentIndex)

  OLD_STDOUT = None
  OLD_STDERR = None

  def mute(self):
    if not self.muteAgents: return
    global OLD_STDOUT, OLD_STDERR
    import cStringIO
    OLD_STDOUT = sys.stdout
    OLD_STDERR = sys.stderr
    sys.stdout = cStringIO.StringIO()
    sys.stderr = cStringIO.StringIO()

  def unmute(self):
    if not self.muteAgents: return
    global OLD_STDOUT, OLD_STDERR
    sys.stdout.close()
    sys.stderr.close()
    # Revert stdout/stderr to originals
    sys.stdout = OLD_STDOUT
    sys.stderr = OLD_STDERR


  def run( self ):
    self.display.initialize(self.state.data)
    self.numMoves = 0

    ###self.display.initialize(self.state.makeObservation(1).data)
    # inform learning agents of the game start
    for i in range(len(self.agents)):
      agent = self.agents[i]
      if not agent:
        # this is a null agent, meaning it failed to load
        # the other team wins
        self._agentCrash(i, quiet=True)
        return
      if ("registerInitialState" in dir(agent)):
        self.mute()
        if self.catchExceptions:
          try:
            timed_func = TimeoutFunction(agent.registerInitialState, int(self.rules.getMaxStartupTime(i)))
            try:
              start_time = time.time()
              timed_func(self.state.deepCopy())
              time_taken = time.time() - start_time
              self.totalAgentTimes[i] += time_taken
            except TimeoutFunctionException:
              print "Agent %d ran out of time on startup!" % i
              self.unmute()
              self.agentTimeout = True
              self._agentCrash(i, quiet=True)
              return
          except Exception,data:
            self.unmute()
            self._agentCrash(i, quiet=True)
            return
        else:
          agent.registerInitialState(self.state.deepCopy())
        ## TODO: could this exceed the total time
        self.unmute()

    agentIndex = self.startingIndex
    numAgents = len( self.agents )

    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[agentIndex]
      move_time = 0
      skip_action = False
      # Generate an observation of the state
      if 'observationFunction' in dir( agent ):
        self.mute()
        if self.catchExceptions:
          try:
            timed_func = TimeoutFunction(agent.observationFunction, int(self.rules.getMoveTimeout(agentIndex)))
            try:
              start_time = time.time()
              observation = timed_func(self.state.deepCopy())
            except TimeoutFunctionException:
              skip_action = True
            move_time += time.time() - start_time
            self.unmute()
          except Exception,data:
            self.unmute()
            self._agentCrash(agentIndex, quiet=True)
            return
        else:
          observation = agent.observationFunction(self.state.deepCopy())
        self.unmute()
      else:
        observation = self.state.deepCopy()

      # Solicit an action
      action = None
      self.mute()
      if self.catchExceptions:
        try:
          timed_func = TimeoutFunction(agent.getAction, int(self.rules.getMoveTimeout(agentIndex)) - int(move_time))
          try:
            start_time = time.time()
            if skip_action:
              raise TimeoutFunctionException()
            action = timed_func( observation )
          except TimeoutFunctionException:
            print "Agent %d timed out on a single move!" % agentIndex
            self.agentTimeout = True
            self.unmute()
            self._agentCrash(agentIndex, quiet=True)
            return

          move_time += time.time() - start_time

          if move_time > self.rules.getMoveWarningTime(agentIndex):
            self.totalAgentTimeWarnings[agentIndex] += 1
            print "Agent %d took too long to make a move! This is warning %d" % (agentIndex, self.totalAgentTimeWarnings[agentIndex])
            if self.totalAgentTimeWarnings[agentIndex] > self.rules.getMaxTimeWarnings(agentIndex):
              print "Agent %d exceeded the maximum number of warnings: %d" % (agentIndex, self.totalAgentTimeWarnings[agentIndex])
              self.agentTimeout = True
              self.unmute()
              self._agentCrash(agentIndex, quiet=True)

          self.totalAgentTimes[agentIndex] += move_time
          #print "Agent: %d, time: %f, total: %f" % (agentIndex, move_time, self.totalAgentTimes[agentIndex])
          if self.totalAgentTimes[agentIndex] > self.rules.getMaxTotalTime(agentIndex):
            print "Agent %d ran out of time! (time: %1.2f)" % (agentIndex, self.totalAgentTimes[agentIndex])
            self.agentTimeout = True
            self.unmute()
            self._agentCrash(agentIndex, quiet=True)
            return
          self.unmute()
        except Exception,data:
          self.unmute()
          self._agentCrash(agentIndex)
          return
      else:
        action = agent.getAction(observation)
      self.unmute()

      # Execute the action
      self.moveHistory.append( (agentIndex, action) )
      if self.catchExceptions:
        try:
          self.state = self.state.generateSuccessor( agentIndex, action )
        except Exception,data:
          self._agentCrash(agentIndex)
          return
      else:
        self.state = self.state.generateSuccessor( agentIndex, action )

      # Change the display
      self.display.update( self.state.data )
      ###idx = agentIndex - agentIndex % 2 + 1
      ###self.display.update( self.state.makeObservation(idx).data )

      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)
      # Track progress
      if agentIndex == numAgents + 1: self.numMoves += 1
      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents

      if _BOINC_ENABLED:
        boinc.set_fraction_done(self.getProgress())

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        try:
          self.mute()
          agent.final( self.state )
          self.unmute()
        except Exception,data:
          if not self.catchExceptions: raise
          self.unmute()
          print "Exception",data
          self._agentCrash(agent.index)
          return
    self.display.finish()

def runGames( layout, pacman, ghosts, display, numGames, record, numTraining = 0, catchExceptions=False, timeout=30 ):
  import __main__
  __main__.__dict__['_display'] = display

  rules = ClassicGameRules(timeout)
  games = []

  for i in range( numGames ):
    beQuiet = i < numTraining
    if beQuiet:
        # Suppress output and graphics
        import textDisplay
        gameDisplay = textDisplay.NullGraphics()
        rules.quiet = True
    else:
        gameDisplay = display
        rules.quiet = False
    game = rules.newGame(layout, pacman, ghosts, gameDisplay, beQuiet, catchExceptions)
    game.run()
    if not beQuiet: games.append(game)

    if record:
      import time, cPickle
      fname = ('recorded-game-%d' % (i + 1)) +  '-'.join([str(t) for t in time.localtime()[1:6]])
      f = file(fname, 'w')
      components = {'layout': layout, 'actions': game.moveHistory}
      cPickle.dump(components, f)
      f.close()

  if (numGames-numTraining) > 0:
    scores = [game.state.getScore() for game in games]
    wins = [game.state.isWin() for game in games]
    winRate = wins.count(True)/ float(len(wins))
    if True:
      print 'Average Score:', sum(scores) / float(len(scores))
      print 'Scores:       ', ', '.join([str(score) for score in scores])
      print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate)
      print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])

  return games

class ClassicGameRules:

  def __init__(self, timeout=30):
    self.timeout = timeout

  def newGame( self, layout, pacmanAgent, ghostAgents, display, quiet = False, catchExceptions=False):
    agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
    initState = GameState()
    initState.initialize( layout, len(ghostAgents) )
    game = Game(agents, display, self, catchExceptions=catchExceptions)
    game.state = initState
    self.initialState = initState.deepCopy()
    self.quiet = quiet
    return game

  def process(self, state, game):

    if state.isWin(): self.win(state, game)
    if state.isLose(): self.lose(state, game)

  def win( self, state, game ):
    if not self.quiet: print "Pacman emerges victorious! Score: %d" % state.data.score
    game.gameOver = True

  def lose( self, state, game ):
    if not self.quiet: print "Pacman died! Score: %d" % state.data.score
    game.gameOver = True

  def getProgress(self, game):
    return float(game.state.getNumFood()) / self.initialState.getNumFood()

  def agentCrash(self, game, agentIndex):
    if agentIndex == 0:
      print "Pacman crashed"
    else:
      print "A ghost crashed"

  def getMaxTotalTime(self, agentIndex):
    return self.timeout

  def getMaxStartupTime(self, agentIndex):
    return self.timeout

  def getMoveWarningTime(self, agentIndex):
    return self.timeout

  def getMoveTimeout(self, agentIndex):
    return self.timeout

  def getMaxTimeWarnings(self, agentIndex):
    return 0

class AgentRules:

  PACMAN_SPEED=1

  def getLegalActions( state ):

    possibleActions = Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
    if Directions.STOP in possibleActions:
      possibleActions.remove( Directions.STOP )
    return possibleActions
  getLegalActions = staticmethod( getLegalActions )

  def applyAction( state, action ):

    legal = PacmanRules.getLegalActions( state )
    if action not in legal:
      raise Exception("Illegal action " + str(action))

    pacmanState = state.data.agentStates[0]

    # Update Configuration
    vector = Actions.directionToVector( action, PacmanRules.PACMAN_SPEED )
    pacmanState.configuration = pacmanState.configuration.generateSuccessor( vector )

    # Eat
    next = pacmanState.configuration.getPosition()
    nearest = nearestPoint( next )
    if manhattanDistance( nearest, next ) <= 0.5 :
      # Remove food
      PacmanRules.consume( nearest, state )
  applyAction = staticmethod( applyAction )

  def consume( position, state ):
    x,y = position
    # Eat food
    if state.data.food[x][y]:
      state.data.scoreChange += 10
      state.data.food = state.data.food.copy()
      state.data.food[x][y] = False
      state.data._foodEaten = position
      # TODO: cache numFood?
      numFood = state.getNumFood()
      if numFood == 0 and not state.data._lose:
        state.data.scoreChange += 500
        state.data._win = True
    # Eat capsule
    if( position in state.getCapsules() ):
      state.data.capsules.remove( position )
      state.data._capsuleEaten = position
      # Reset all ghosts' scared timers
      for index in range( 1, len( state.data.agentStates ) ):
        state.data.agentStates[index].scaredTimer = SCARED_TIME
  consume = staticmethod( consume )
 """