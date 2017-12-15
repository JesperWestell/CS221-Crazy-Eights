# CS221-Crazy-Eights
CS221 Course Project on developing a Crazy Eights playing AI

# Commands
Edit arguments in run.py and run
```bash
python run.py
```
or use evaluate.py:

Example: play a game against PruningAgent
```bash
python evaluate.py -n 1 -a KeyboardAgent,PruningAgent -v 5
```

Example: run 100 games between PruningAgent and oracle
```bash
python evaluate.py -n 100 -a PruningAgent,OracleAgent -v 3
```

# Code

## evaluate.py
Contains code capable of running multiple games, and evaluate the results. Can
be called from the terminal, or run from run.py, if you don't want to add
arguments to the call.

## run.py
Script used to call on evaluate.py with predefined arguments.

## crazy_eights_game.py
Contains the classes CrazyEightsGame, GameState, Observer, together with code
used by these classes.

## game.py
Contains the code that is needed to run one instance of a game.
Creates a CrazyEightsGame object that keeps track of the state of the game, and
orders the agents to make moves.

## game_rules.py
Contains different sets of rules a game can have.
ClassicGameRules is the most common rules to be used.

## agent.py
Contains the abstract class Agent, used by all agents.

## baseline_agent.py
Contains all logic behind the baseline.

## oracle.py
Contains all logic behind the oracle.

## keyboard_agent.py
Contains all logic behind KeyboardAgent.

## basic_minimax_agent.py
Contains all logic behind BasicMinimaxAgent.

## rl_agent.py
Contains all logic behind RLAgent.

## pruning_agent.py
Contains all logic behind PruningAgent.

## QLPruneAgent.py
Contains the unfinished work for the Q-learning agent.

## learner.py
Contains all code used to learn the parameters for both the evaluation function
used by RLAgent, and for the state-action probability estimator used by
PruningAgent.

## Qtraining.py
Similar to learner.py this file contains the functions to learn the Q-values
for the Q-learning agent.

## util.py
Contains helper functions used by many of the agents.

## rl_weights.txt
Contains the weights used by the evaluation function used by RLAgent. Readable
by pickle.

## state_weight.txt
Contains the weights used by the state-action probability estimator used by
PruningAgent. Readable by pickle.

## action_and_state_weights.txt
Contains the weights used by the state-action probability estimator used by
PruningAgent. Readable by pickle.



