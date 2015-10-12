from gamelogic import Gamelogic
import heapq

class Solver():
	'''

	'''


	def __init__(self):
		'''

		'''
		self.directions = {1: "RIGHT", 2: "LEFT", 3: "UP", 4: "DOWN"}
		self.logic = Gamelogic()
		self.neighbours = list()
		heapq.heapify(self.neighbours)

	def move(self, direction, board):
		'''

		'''
		return self.logic.move(direction, board)

	def solve(self, board):
		'''

		'''
		self.neighbours = list()
		heapq.heapify(self.neighbours)
		if not self.logic.is_game_over(board):
			self.minimax(board, 1, True)
			board = heapq.heappop(self.neighbours)[1]
			board = self.logic.append_random_number(board)
			return board

			#Return some board

	def get_neighbours(self, board):
		'''

		'''
		neighbours = list()
		for move in self.directions:
			neighbour = self.logic.check_move(self.directions[move], board)
			print(self.directions[move], neighbour)
			if neighbour != None:
				neighbours.append(neighbour)
		return neighbours

	def heuristic(self, board):
		'''

		'''
		#Currently just counts the amount of white spaces.
		#TODO, figure out good heuristic.

		h = 16
		for row in board:
			h -= row.count(0)
		return h

	def random_permutations(self, board):
		'''

		'''
		permutations = self.logic.append_all_random_numbers(board)
		return permutations

	def expectimax(self, board, depth, maximizing_player):
		'''

		'''
		if depth == 0:
			return self.heuristic(board)
		if maximizing_player:
			#Return value of maximum-valued child node
			let α := -∞
			alpha = float("-inf")
			for neighbour in self.get_neighbours(board):
				alpha = max(α, expectimax(neighbour, depth - 1, False))
		else:
			# Return weighted average of all child nodes' values
			alpha = 0
			for neighbour in self.get_neighbours(board):
				alpha = alpha + (Probability[child] * expectimax(child, depth-1))
		return alpha

if __name__ == "__main__":
	solver = Solver()
	print("-----------")
	print(solver.solve([[0, 0, 0, 0],[0, 2, 0, 2],[0, 0, 0, 0],[0, 0, 0, 0]]))