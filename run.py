import evaluate
import timeit

games = 100
#agents = 'BasicMinimaxAgent,OracleAgent'
#agents = 'PruningMinimaxAgent,OracleAgent'
#agents = 'RLProbAgent,OracleAgent'
#agents = 'RLPruningAgent,OracleAgent'
#agents = 'OracleAgent,BasicMinimaxAgent'
#agents = 'RLAgent,OracleAgent'
#agents = 'RLAgent,BaselineAgent'
#agents = 'BaselineAgent,OracleAgent'
agents = 'KeyboardAgent,BaselineAgent'
verbose = 5
fixseed = 'False'
params = '-n %s -a %s -v %s -f %s' % (games,agents,verbose,fixseed)
start = timeit.default_timer()
evaluate.runGames(**evaluate.readCommand(params.split(' ')))
end = timeit.default_timer()
print
print('Time per game: {0}'.format((end - start)/games))

