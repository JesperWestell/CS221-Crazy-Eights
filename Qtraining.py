from game import Game
import game_rules
import sys,random,os,collections
from keyboard_agent import KeyboardAgent
from baseline_agent import BaselineAgent
from oracle import OracleAgent
from basic_minimax_agent import BasicMinimaxAgent
from rl_agent import RLAgent
from QLAgent import QLAgent
from QLPruneAgent import QLPruneAgent
from QLMinMaxAgent import QLMinMaxAgent


def runMinMaxGames(numGames, verbose, startState = None):
    agents = ["OracleAgent", "QLMinMaxAgent"]
    game = Game(agents=[ OracleAgent(), BasicMinimaxAgent()], verbose=verbose>=3)
    times_won = [0, 0]
    print agents
    countGames = 0
    for i in range(numGames):
        countGames += 1
        winner = game.run(startState)
        times_won[winner] += 1
        if verbose >= 2:
            print_winnings(times_won,agents)
    if verbose >= 1:
        print '\n-- Final Score Before Learning'
        print_winnings(times_won, agents)
    print times_won
    return times_won



def runLearnGames(numGames, verbose, startState = None):
    agentsNames = ["OracleAgent", "QLPruneAgent"]
    agents = [OracleAgent(index=0), QLPruneAgent(index=1, learning = True)]
    game = Game(agents = agents, verbose=verbose>=3)
    times_won = [0, 0]
    countGames = 0
    for i in range(numGames):
        countGames += 1
        if countGames == 500:
            agents[1].epsilon = 0.2
            print 'epsilon now', agents[1].epsilon
        if countGames%300 == 0:
            print '300 more games'
            print_winnings(times_won, agentsNames)
        winner, learningDict = game.run(startState)
        times_won[winner] += 1
        if verbose >= 2:
            print_winnings(times_won, agentsNames)
    print 'Qtable values', learningDict.values()
    if verbose >= 1:
        print '\n-- Final Score Before Learning'
        print_winnings(times_won, agentsNames)
    print times_won
    return times_won


def runLearnMinMaxGames(numGames, verbose, startState = None):
    agentsNames = ["OracleAgent", "QLMinMaxAgent"]
    agents = [OracleAgent(), QLMinMaxAgent(learning = True)]
    game = Game(agents = agents, verbose=verbose>=3)
    times_won = [0, 0]
    countGames = 0
    for i in range(numGames):
        countGames += 1
        if countGames == 500:
            agents[1].epsilon = 0.2
        if countGames%300 == 0:
            print '300 more games'
            print_winnings(times_won, agentsNames)
        winner, learningDict = game.run(startState)
        times_won[winner] += 1
        if verbose >= 2:
            print_winnings(times_won, agentsNames)
    print 'Qtable values', learningDict.values()
    if verbose >= 1:
        print '\n-- Final Score Before Learning'
        print_winnings(times_won, agentsNames)
    print 'played: '+ str(countGames)+' games.'
    print times_won
    return times_won

def print_winnings(times_won, agents):

    totalWinnings = 0
    for i,a in enumerate(agents):
        print a + ' winnings: ' + str(times_won[i])
        totalWinnings += times_won[i]
    winRate = 100 *(1- times_won[0] / float(
        totalWinnings))
    print 'Win Rate: %.2f %%' % winRate

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
    #args = readCommand(sys.argv[1:])  # Get game components based on input
    #runMinMaxGames(50, verbose = 1)
    runLearnGames(500, verbose = 1)
    #runLearnMinMaxGames(10000, verbose = 1)

if __name__ == '__main__':
    main()

