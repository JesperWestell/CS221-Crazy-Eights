import evaluate
import timeit

games = 5
#agents = 'MinimaxAgent,BaselineAgent'
#agents = 'MinimaxAgent,OracleAgent'
#agents = 'BasicMinimaxAgent,OracleAgent,BaselineAgent'
#agents = 'MinimaxAgent,MinimaxAgent,BaselineAgent'
#agents = 'RLAgent,BasicMinimaxAgent,BaselineAgent'
agents = 'KeyboardAgent,OracleAgent'
verbose = 2
fixseed = 'False'
params = '-n %s -a %s -v %s -f %s' % (games,agents,verbose,fixseed)
start = timeit.default_timer()
evaluate.runGames(**evaluate.readCommand(params.split(' ')))
end = timeit.default_timer()
print
print('Time per game: {0}'.format((end - start)/games))

