import tictactoe

def toOX(player):
  if player == tictactoe.PlayerCircle:
    return "O"
  elif player == tictactoe.PlayerCross:
    return "X"
  else:
    return " "

def sPrintRow(row):
  return "%s | %s | %s" % (toOX(row[0]), toOX(row[1]), toOX(row[2]))

def printBoard(state):
  print "     a   b   c"
  print "   -------------"
  print("3  | %s |" % sPrintRow(state.s[0:3]))
  print "   -------------"
  print("2  | %s |" % sPrintRow(state.s[3:6]))
  print "   -------------"
  print("1  | %s |" % sPrintRow(state.s[6:9]))
  print "   -------------"

def getUserAction(user, state):
  inp = raw_input("Your turn (%s): " % toOX(user))

  while True:
    if len(inp) < 2:
      inp = raw_input("Wrong move '%s', please try again: " % inp)
      continue
    col = inp[0]
    row = inp[1]

    pos = -1
    if col == "a" and row == "3":
      pos = 0
    elif col == "b" and row == "3":
      pos =  1
    elif col == "c" and row == "3":
      pos = 2
    elif col == "a" and row == "2":
      pos = 3
    elif col == "b" and row == "2":
      pos = 4
    elif col == "c" and row == "2":
      pos = 5
    elif col == "a" and row == "1":
      pos = 6
    elif col == "b" and row == "1":
      pos = 7
    elif col == "c" and row == "1":
      pos = 8
    else:
      inp = raw_input("Wrong move '%s', please try again: " % inp)
      continue

    for unoccupied in state.unoccupied():
      if pos == unoccupied:
        return pos

    inp = raw_input("Wrong move '%s', please try again: " % inp)


def printWinner(state, user):
  winner = state.winner()
  if winner == user:
    print "You won!"
  elif winner == tictactoe.PlayerNone:
    print "Draw"
  else:
    print "You lost :("

  print ""


def run(user, opponent, opponentFirst):
  s = tictactoe.State()

  if opponentFirst:
    a = tictactoe.chooseAction(opponent, s, 0)
    s = tictactoe.takeAction(opponent.player, s, a)

  printBoard(s)
  while True:
    a = getUserAction(user, s)
    s = tictactoe.takeAction(user, s, a)
    printBoard(s)
    if s.terminal():
      break

    a = tictactoe.chooseAction(opponent, s, 0)
    s = tictactoe.takeAction(opponent.player, s, a)
    printBoard(s)
    if s.terminal():
      break

  printWinner(s, user)
