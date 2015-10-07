from gamelogic import Gamelogic

class Solver():
	'''

	'''


	def __init__(self, board):
		'''

		'''
		self.directions = {1: "RIGHT", 2: "LEFT", 3: "UP", 4: "DOWN"}
		self.logic = Gamelogic(board)
		self.board = board

	def move(self, direction):
		'''

		'''
		return self.logic.move(direction)

	def solve(self, board):
		'''

		'''
		if not self.logic.is_game_over():
			self.get_neighbours()
			

			#Return some board

	def get_neighbours(self):
		'''

		'''
		neighbours = list()
			for move in range(self.directions):
				neighbours.append(logic.check_move(self.directions[move]))

	def heuristic(self):
		'''

		'''
		#Currently just counts the amount of white spaces.
		#TODO, figure out good heuristic.

		h = 0
		for row in self.board:
			h += row.count(0)
		return h

solver = Solver([[0,1,0],[0,1,2]])
print(solver.heuristic())

