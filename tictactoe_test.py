import unittest

from tictactoe import *

class TestTicTacToe(unittest.TestCase):

  def testStateEq(self):
    s1 = State()
    s1.s = (PlayerCircle, PlayerNone, PlayerNone,
            PlayerNone,   PlayerNone, PlayerNone,
            PlayerNone,   PlayerNone, PlayerNone, )
    s2 = State()
    s2.s = (PlayerCircle, PlayerNone, PlayerNone,
            PlayerNone,   PlayerNone, PlayerNone,
            PlayerNone,   PlayerNone, PlayerNone, )
    self.assertEqual(s1, s2)

    s2.s = (PlayerCircle, PlayerCircle, PlayerNone,
            PlayerNone,   PlayerNone,   PlayerNone,
            PlayerNone,   PlayerNone,   PlayerNone, )
    self.assertNotEqual(s1, s2)

  def testStateTerminal(self):
    s = State()
    s.s = (PlayerCross,  PlayerCircle, PlayerCross,
           PlayerCross,  PlayerCircle, PlayerCircle,
           PlayerCircle, PlayerCross,  PlayerCircle, )

    # s is a draw, check that it is a terminal state.
    self.assertTrue(s.terminal())

  def testTakeAction(self):
    s = State()
    s.s = (PlayerCross,  PlayerCircle, PlayerCross,
           PlayerCross,  PlayerNone,   PlayerCircle,
           PlayerCircle, PlayerCross,  PlayerNone, )

    # Check that takeAction raises an error if we take an action on states that are occupied
    for pos in (0, 1, 2, 3, 5, 6, 7):
      with self.assertRaises(ValueError):
        takeAction(PlayerCircle, s, pos)


  def testStateActionsUpdate(self):
    state = State()
    state.s = (PlayerCross,  PlayerNone,  PlayerCross,
               PlayerCross,  PlayerNone,  PlayerCircle,
               PlayerCircle, PlayerCross, PlayerNone, )
    sa = StateActions(state)

    # assert that the update method of a StateActions does update itself
    self.assertEqual(sa.get(1), ScoreDraw)
    sa.update(1, ScoreWin)
    self.assertEqual(sa.get(1), ScoreWin)


  def testStateActionsBest(self):
    state = State()
    state.s = (PlayerCross,  PlayerNone,  PlayerCross,
               PlayerCross,  PlayerNone,  PlayerCircle,
               PlayerCircle, PlayerCross, PlayerNone, )
    
    sa = StateActions(state)
    sa.update(1, 2.1)
    sa.update(4, 2.9)
    sa.update(8, 2.5)

    # assert that the best action for state is position 4 with a score of 2.9
    best = sa.best()
    self.assertEqual(best.pos, 4)
    self.assertEqual(best.score, 2.9)


  def testActionValueFunc(self):
    q = ActionValueFunc(PlayerCircle)

    state = State()
    state.s = (PlayerCross,  PlayerNone,  PlayerCross,
               PlayerCross,  PlayerNone,  PlayerCircle,
               PlayerCircle, PlayerCross, PlayerNone, )

    action = 8
    score = ScoreWin + 0.6

    # assert that the update method of an ActionValueFunc does update itself
    self.assertEqual(q.Q(state, action), ScoreDraw)
    q.update(state, action, score)
    self.assertEqual(q.Q(state, action), score)

    # assert that the best score is indeed the one we updated just now
    self.assertEqual(q.best(state), score)
