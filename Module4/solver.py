from gamelogic import Gamelogic
import heapq
import copy

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
		if board != None:
			self.neighbours = list()
			heapq.heapify(self.neighbours)
			for neighbour in self.get_neighbours(board):
				heapq.heappush(self.neighbours, (self.expectimax(neighbour, 3, False), neighbour))
			board = heapq.heappop(self.neighbours)[1]
			board = self.logic.append_random_number(board)
			return board

	def get_neighbours(self, board):
		'''

		'''
		neighbours = list()
		for move in self.directions:
			neighbour = self.logic.check_move(self.directions[move], copy.deepcopy(board))
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

	def probability_of_reaching_node(self, key, board):
		'''

		'''
		zero_count = 0
		for row in board:
			zero_count += row.count(0)
		if key == 2:
			return 0.9 / zero_count
		elif key == 4:
			return 0.1 / zero_count

	def expectimax(self, board, depth, maximizing_player):
		'''

		'''
		if depth == 0:
			h = self.heuristic(board)
			#SKJOENNER IKKE HVORDAN JEG SKAL HEAPPUSHE BARE DE 4 FOERSTE MAXNODENE,
			#OG MED HVOR FAAR JEG HEURISTIKKEN DEMS FRA???
			#heapq.heappush(self.neighbours, (h, board))
			return h
		if maximizing_player:
			#Return value of maximum-valued child node
			alpha = float("-inf")
			for neighbour in self.get_neighbours(board):
				alpha = max(alpha, self.expectimax(neighbour, depth - 1, False))
		elif maximizing_player == False:
			# Return weighted average of all child nodes' values
			alpha = 0
			neighbours = self.logic.append_all_random_numbers(board)
			for key in neighbours.keys():
				for neighbour in neighbours[key]:
					alpha += (self.probability_of_reaching_node(key, board) * self.expectimax(neighbour, depth - 1, True))
		#print("alpha")
		return alpha

if __name__ == "__main__":
	solver = Solver()
	logic = Gamelogic()
	print("-----------")
	board = [[2, 0, 0, 0],[0, 2, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
	neighbours = solver.get_neighbours(board)
	#print(neighbours)