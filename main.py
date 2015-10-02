import argparse
import random

import game
import tictactoe
import train

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--algo", help="the training algorithm, sarsa for SARSA and qlearning for Q-learning")
  args = parser.parse_args()
  if args.algo == "sarsa":
    algo = train.SARSA
    print "Training using SARSA algorithm"
  else:
    algo = train.QLearning
    print "Training using Q-learning algorithm"

  circle = tictactoe.ActionValueFunc(tictactoe.PlayerCircle)
  cross = tictactoe.ActionValueFunc(tictactoe.PlayerCross)
  train.run(algo, circle, cross)

  print "Training completed, game starting..."
  while True:
    user = raw_input("Please choose a player, O or X: ")
    if user == "X" or user == "x":
      user = tictactoe.PlayerCross
      opponent = circle
      print "You are player X"
    else:
      user = tictactoe.PlayerCircle
      opponent = cross
      print "You are player O"

    opponentFirst = True
    yn = raw_input("Do you want to go first? Y for yes, N for no, others for either way: ")
    if yn == "Y" or yn == "y":
      opponentFirst = False
    elif yn == "N" or yn == "n":
      opponentFirst = True
    else:
      if random.random() < 0.5:
        opponentFirst = False

    game.run(user, opponent, opponentFirst)

if __name__ == '__main__':
  main()
