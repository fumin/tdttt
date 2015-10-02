import unittest

from tictactoe import *
from train import *

class TestTrain(unittest.TestCase):

  def testSARSA(self):
    q = ActionValueFunc(PlayerCircle)
    state = State()
    state.s = (PlayerCross,  PlayerNone,  PlayerCross,
               PlayerCross,  PlayerNone,  PlayerCircle,
               PlayerCircle, PlayerCross, PlayerCircle, )
    action = 4 # the center position
    newState = State()
    newState.s = (PlayerCross,  PlayerCross,  PlayerCross,
                  PlayerCross,  PlayerCircle, PlayerCircle,
                  PlayerCircle, PlayerCross,  PlayerCircle, )
    epsilon = 0.0
    alpha = 0.1
    gamma = 0.9

    # assert that SARSA does update the action-value function to the expected value
    self.assertEqual(q.Q(state, action), ScoreDraw)
    SARSA(q, state, action, newState, epsilon, alpha, gamma)
    self.assertEqual(q.Q(state, action), -0.19)


  def testQLearning(self):
    q = ActionValueFunc(PlayerCircle)
    state = State()
    state.s = (PlayerCross,  PlayerNone,  PlayerCross,
               PlayerCross,  PlayerNone,  PlayerCircle,
               PlayerCircle, PlayerCross, PlayerCircle, )
    action = 4 # the center position
    newState = State()
    newState.s = (PlayerCross,  PlayerCross,  PlayerCross,
                  PlayerCross,  PlayerCircle, PlayerCircle,
                  PlayerCircle, PlayerCross,  PlayerCircle, )
    alpha = 0.1
    gamma = 0.9

    # assert that QLearning does update the action-value function to the expected value
    self.assertEqual(q.Q(state, action), ScoreDraw)
    QLearning(q, state, action, newState, alpha, gamma)
    self.assertEqual(q.Q(state, action), -0.1)
