from gamelogic import Gamelogic

class Solver():
	'''

	'''


	def __init__(self, board):
		'''

		'''
		self.logic = Gamelogic(board)

	def move(self, direction):
		'''

		'''
		return self.logic.move(direction)

	def solve(self, board):
		'''

		'''

if __name__ == "__main__":
	board = [[1, 0, 2, 2],
			[0, 2, 0, 2],
			[2, 2, 2, 2],
			[4, 8, 0, 0]]
	solver = Solver(board)
