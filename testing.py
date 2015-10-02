import unittest

import tictactoe_test
import train_test

if __name__ == '__main__':
  suite = [ unittest.TestLoader().loadTestsFromTestCase(tictactoe_test.TestTicTacToe) ]
  suite.append( unittest.TestLoader().loadTestsFromTestCase(train_test.TestTrain) )
  unittest.TextTestRunner().run(unittest.TestSuite(suite))
