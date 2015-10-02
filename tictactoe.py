import random

# Players represent the owners of positions in a Tic Tac Toe grid.
# PlayerNone indicates that a position has not been occupied.
PlayerNone = 0
# PlayerCircle indicates that a position has been taken by player circle.
PlayerCircle = 1
# PlayerCross indicates that a position has been taken by player cross.
PlayerCross = 2

# A State is a snapshot of the grid in a Tic Tac Toe game.
# Such a grid is represented by an immutable tuple whose indices run row by row as in the following diagram:
#
#   0  1  2
#   3  4  5
#   6  7  8
#
# The values of each position in this tuple are either PlayerNone, PlayerCircle or PlayerCross,
# indicating the respective ownership of this position on the grid.
#
# For example, state[4] == PlayerCross means that a cross has been drawn on the center of the grid;
# likewise, state[6] == PlayerNone means that the lower left position is not occupied yet.
class State:
  def __init__(self):
    self.s = (PlayerNone, PlayerNone, PlayerNone,
              PlayerNone, PlayerNone, PlayerNone,
              PlayerNone, PlayerNone, PlayerNone, )

  def __eq__(self, other):
    return self.s == other.s

  def __hash__(self):
    return hash(self.s)

  # winner returns the winner of a state according to the rules of Tic Tac Toe.
  # If no winner has been determined in the current state yet, PlayerNone is returned.
  def winner(self):
    # Horizontal lines
    if self.s[0] != PlayerNone and self.s[0] == self.s[1] and self.s[0] == self.s[2]:
      return self.s[0]
    if self.s[3] != PlayerNone and self.s[3] == self.s[4] and self.s[3] == self.s[5]:
      return self.s[3]
    if self.s[6] != PlayerNone and self.s[6] == self.s[7] and self.s[6] == self.s[8]:
      return self.s[6]

    # Vertical lines
    if self.s[0] != PlayerNone and self.s[0] == self.s[3] and self.s[0] == self.s[6]:
      return self.s[0]
    if self.s[1] != PlayerNone and self.s[1] == self.s[4] and self.s[1] == self.s[7]:
      return self.s[1]
    if self.s[2] != PlayerNone and self.s[2] == self.s[5] and self.s[2] == self.s[8]:
      return self.s[2]

    # Diagonal lines
    if self.s[0] != PlayerNone and self.s[0] == self.s[4] and self.s[0] == self.s[8]:
      return self.s[0]
    if self.s[6] != PlayerNone and self.s[6] == self.s[4] and self.s[6] == self.s[2]:
      return self.s[6]

    return PlayerNone

  # terminal returns whether or not this state contains no possible future moves.
  def terminal(self):
    if self.winner() != PlayerNone:
      return True

    for player in self.s:
      if player == PlayerNone:
        return False

    return True

  # unoccupied returns the list of positions that are available.
  def unoccupied(self):
    res = []
    for pos, player in enumerate(self.s):
      if player == PlayerNone:
        res.append(pos)
    return res


# takeAction marks a position on a state as belonging to a player.
# A new state is returned representing the effect of taking such an action.
def takeAction(player, state, pos):
  if player != PlayerCircle and player != PlayerCross:
    raise ValueError("unexpected player: %s" % player)

  if state.s[pos] != PlayerNone:
    raise ValueError("invalid position %s for state %s" % (pos, state))

  l = list(state.s)
  l[pos] = player

  newState = State()
  newState.s = tuple(l)
  return newState


# ScoreWin is the score given to players who won a game.
ScoreWin = 1.0
# ScoreDraw is the score given to players who had a draw in a game.
ScoreDraw = 0.0
# ScoreLose is the score given to players who lost a game.
ScoreLose = -1.0

# observeReward returns the immediate reward to players,
# with respect to the current state and the rules of Tic Tac Toe.
def observeReward(player, state):
  if player != PlayerCircle and player != PlayerCross:
    raise ValueError("unexpected player: %s" % player)

  winner = state.winner()
  if winner == player:
    return ScoreWin
  elif winner == PlayerNone:
    return ScoreDraw
  else:
    return ScoreLose


class PositionScore:
  def __init__(self, position, score):
    self.pos = position
    self.score = score

# A StateActions is a collection of the possible actions and their scores of a state.
# It answers queries for the best action with the highest score, with respect to a given state.
class StateActions:
  def __init__(self, state):
    # We use an ordinary list as the backing data structure,
    # since the possible number of items stored is small and always less than 9.
    self.a = []

    # We immediately store all possible positions of this state with the default value of ScoreDraw into our list,
    # as opposed to leaving it empty and lazy inserting items later on when we want to change scores.
    # This way, it is easier and more straight forward to determine the best action with the highest score.
    for pos in state.unoccupied():
      self.a.append(PositionScore(pos, ScoreDraw))

  def update(self, pos, score):
    # Since we initialize our list to contain all positions in the beginning,
    # we are guaranteed to find the specified to-be-updated position.
    for ps in self.a:
      if ps.pos == pos:
        ps.score = score
        break

  def get(self, pos):
    # Since we initialize our list to contain all positions in the beginning,
    # we are guaranteed to find the specified position.
    for ps in self.a:
      if ps.pos == pos:
        return ps.score

  # best returns the position with the highest score.
  # In case there are more than one positions sharing the same highest score,
  # we simply randomly pick one among them.
  def best(self):
    self.a.sort(key=lambda ps: ps.score, reverse=True)

    top = [self.a[0]]
    for ps in self.a[1:]:
      if ps.score == self.a[0]:
        top.append(ps)
      else:
        break

    return random.choice(top)


# An ActionValueFunc is an action-value function in Q-learning.
# For more details about its theory, please see
# http://webdocs.cs.ualberta.ca/~sutton/book/ebook/node65.html
class ActionValueFunc:
  def __init__(self, player):
    self.player = player
    self.stateActions = {}

  # Q returns the score or a (state, action) pair.
  def Q(self, state, pos):
    if state not in self.stateActions:
      return ScoreDraw

    sa = self.stateActions[state]
    return sa.get(pos)

  # update updates the score of a (state, action) pair.
  def update(self, state, pos, score):
    if state in self.stateActions:
      sa = self.stateActions[state]
    else:
      sa = StateActions(state)

    sa.update(pos, score)
    self.stateActions[state] = sa

  # best returns the score of the best possible action to be taken with respect to the current state.
  def best(self, state):
    if state not in self.stateActions:
      return ScoreDraw

    sa = self.stateActions[state]
    return sa.best().score


# chooseAction returns the best possible action of a state using the epsilon-greedy algorithm.
# A larger epsilon increases the possibility that a random action will be chosen, thus encouraging exploratory behaviour.
# In contrast, a smaller epsilon encourages exploitary over exploratory behaviour which might be useful in later stages of training
def chooseAction(q, state, epsilon):
  if random.random() < epsilon:
    return random.choice(state.unoccupied())

  if state not in q.stateActions:
    return random.choice(state.unoccupied())

  sa = q.stateActions[state]
  return sa.best().pos
