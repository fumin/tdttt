import math
import random

import tictactoe

# SARSA performs an update to an action-value function according to the SARSA algorithm.
def SARSA(q, s, a, newState, epsilon, alpha, gamma):
  reward = tictactoe.observeReward(q.player, newState)

  if newState.terminal():
    newQ = reward
  else:
    newAction = tictactoe.chooseAction(q, newState, epsilon)
    newQ = q.Q(newState, newAction)

  newScore = q.Q(s, a) + alpha*(reward + gamma*newQ - q.Q(s, a))
  q.update(s, a, newScore)


# QLearning performs an update to an action-value function according to the Q-learning algorithm.
def QLearning(q, s, a, newState, alpha, gamma):
  reward = tictactoe.observeReward(q.player, newState)

  newScore = q.Q(s, a) + alpha*(reward + gamma*q.best(newState) - q.Q(s, a))
  q.update(s, a, newScore)


# runEpisode performs a single training episode by arranging two ActionValueFuncs to play against each other.
#
# The argument algo can be either SARSA or QLearning,
# q is a list of the two ActionValueFuncs,
# epsilon controls the greediness of action selection,
# alpha controls the learning rate of the score updates,
# and gamma is the discount rate of immediate rewards.
#
# The first agent in the argument q moves first in the game.
def runEpisode(algo, q, epsilon, alpha, gamma):
  s = tictactoe.State()
  a = tictactoe.chooseAction(q[0], s, epsilon)
  s1 = tictactoe.takeAction(q[0].player, s, a)
  while True:
    # After the first player has made her move, let the second make his move, too.
    # The resulting state s2 is effectively the outcome of the action taken by the first player earlier.
    # From the first player's point of view, with
    #
    #   * the current state: "s"
    #   * the taken action: "a"
    #   * the new state: "s2"
    #
    # we can update her action-value function according to the algorithm.
    opponentAction = tictactoe.chooseAction(q[1], s1, epsilon)
    s2 = tictactoe.takeAction(q[1].player, s1, opponentAction)

    if algo == SARSA:
      SARSA(q[0], s, a, s2, epsilon, alpha, gamma)
    else:
      QLearning(q[0], s, a, s2, alpha, gamma)

    # Roll forward states and switch sides.
    s = s1
    s1 = s2
    a = opponentAction
    q[0], q[1] = q[1], q[0]

    # When the game ends, due to a time step lag, the player that made the last move has not observed the reward yet.
    # Let her observe the terminal state and update her action-value function before leaving.
    if s1.terminal():
      if algo == SARSA:
        SARSA(q[0], s, a, s1, epsilon, alpha, gamma)
      else:
        QLearning(q[0], s, a, s1, alpha, gamma)
      break


# rewardPerEpisode returns the reward-per-episode of a player.
# The reward is defined with respect to playing against a randomly acting opponent.
def rewardPerEpisode(q, gamma):
  if q.player == tictactoe.PlayerCircle:
    opponent = tictactoe.ActionValueFunc(tictactoe.PlayerCross)
  else:
    opponent = tictactoe.ActionValueFunc(tictactoe.PlayerCircle)

  rpe = 0.0 # reward per episode
  t = 0 # time step
  s = tictactoe.State()

  # Randomly determine whether the player or her opponent should move first.
  if random.random() < 0.5:
    a = tictactoe.chooseAction(opponent, s, 0)
    s = tictactoe.takeAction(opponent.player, s, a)
    t += 1

  while True:
    # Player makes a move and defers observing the reward until her opponent has made his move.
    # Only under the special case where the move is the last move should the player observe reward before exiting.
    a = tictactoe.chooseAction(q, s, 0)
    s1 = tictactoe.takeAction(q.player, s, a)
    t += 1
    if s1.terminal():
      reward = tictactoe.observeReward(q.player, s1)
      rpe += math.pow(gamma, t) * reward
      break

    # Opponent make a move, and the resulting state is observed by player to calculate her reward.
    opponentAction = tictactoe.chooseAction(opponent, s1, 0)
    s2 = tictactoe.takeAction(opponent.player, s1, opponentAction)
    t += 1
    reward = tictactoe.observeReward(q.player, s2)
    rpe += math.pow(gamma, t) * reward

    s = s2
    if s.terminal():
      break

  return rpe


# run runs a number of training episodes for an algorithm on two opposite players, circle and cross.
# The supported algorithms are SARSA and Q-learning.
# The arguments circle and cross are of type tictactoe.ActionValueFunc.
def run(algo, circle, cross):
  alpha = 0.1 # learning rate
  gamma = 0.9 # discount of reward

  rpeCircle = 0.0 # reward per episodes for the circle player
  totalEpisodes = 400000
  for epi in range(totalEpisodes):
    if random.random() < 0.5:
      q = [circle, cross]
    else:
      q = [cross, circle]

    epsilon = 0.1 # epsilon in the epsilon-greedy action selection
    runEpisode(algo, q, epsilon, alpha, gamma)

    rpeCircle += rewardPerEpisode(circle, gamma)
    acc = 1000
    if epi % acc == 0:
      print("episode: %s, reward-per-episode: %s" % (epi, rpeCircle / acc))
      rpeCircle = 0.0
