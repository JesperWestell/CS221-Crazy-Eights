from game import Game
import game_rules
import sys,random,os,collections
from keyboard_agent import KeyboardAgent
from baseline_agent import BaselineAgent
from oracle import OracleAgent
from minimax_agent import MinimaxAgent


def loadAgent(pacman):
  # Looks through all pythonPath Directories for the right module,
  pythonPathStr = os.path.expandvars("$PYTHONPATH")
  if pythonPathStr.find(';') == -1:
    pythonPathDirs = pythonPathStr.split(':')
  else:
    pythonPathDirs = pythonPathStr.split(';')
  pythonPathDirs.append('.')

  for moduleDir in pythonPathDirs:
    if not os.path.isdir(moduleDir): continue
    moduleNames = [f for f in os.listdir(moduleDir) if f.endswith('gent.py') or f.endswith('oracle.py')]
    for modulename in moduleNames:
      try:
        module = __import__(modulename[:-3])
      except ImportError:
        continue
      if pacman in dir(module):
        return getattr(module, pacman)
  raise Exception('The agent ' + pacman + ' is not specified in any file.')

def readCommand(argv):
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('-n', '--numGames', dest='numGames', type='int'
                      , metavar='GAMES', default=1)
    parser.add_option('-a', '--agents', dest='agents',
                      metavar='AGENTS', default='KeyboardAgent OracleAgent')
    parser.add_option('-v', '--verbose', dest='verbose', type='int',
                      metavar='VERBOSE', default=0)
    parser.add_option('-f', '--fixseed', dest='fixRandomSeed',
                      metavar='RANDOM', default=False)

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    # Fix the random seed
    if options.fixRandomSeed == 'True' or options.fixRandomSeed == 'true':
        random.seed('CS221')

    # Choose agents
    agents = options.agents.split(',')
    if len(agents) < 2:
        raise Exception(
            'Must use more than 1 agent! Currently adding %s' % len(agents))
    for a in agents:
        loadAgent(a)

    if options.numGames < 0:
        raise Exception('num games must be positive')
    args['numGames'] = options.numGames
    args['agents'] = agents
    args['verbose'] = options.verbose

    return args

def print_winnings(times_won, agents):
    print
    totalWinnings = 0
    for i,a in enumerate(agents):
        print a + ' winnings: ' + str(times_won[i])
        totalWinnings += times_won[i]
    winRate = 100 * times_won[0] / float(
        totalWinnings)
    print 'Win Rate: %.2f %%' % winRate

def runGames(numGames, agents, verbose):
    instantiated_agents=[eval(a+'()') for a in agents]
    game = Game(agents=instantiated_agents, verbose=verbose>=3)
    times_won = [0 for i in range(len(agents))]
    for i in range(numGames):
        winner = game.run()
        times_won[winner] += 1
        if verbose >= 2:
            print_winnings(times_won,agents)
    if verbose >= 1:
        print '\n-- Final Score --'
        print_winnings(times_won, agents)
    return times_won


def main():
    """
    Arguments to write:
    -n : Number of game
    -a : The two agents you want to play with
        example: "-a OracleAgent,BaselineAgent"
    -v : the verbosity of output. Ranges from 0-3
    -f : If set to True, the game will use a fixed seed
        Good for debugging purposes I guess
    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGames(**args)

if __name__ == '__main__':
    main()