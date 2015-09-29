from board import Board
from gac import GAC
from astar import Astar

import copy

class probleminstance():

	
	'''

	'''
	def __init__(self, contraints = {}, domains = {}):
		'''

		'''
		#A* INFO
		self.h = 0
		self.g = 0
		self.f = 0
		self.predecessor = None
		self.neighbours = []

		#GAC INFO
		self.constraints = contraints
		self.domains = domains


		#init gac
		self.gac = GAC()
		self.domains = self.gac.initialize(self.constraints, self.domains)

		astar = Astar(self)
		while True:
			current = astar.solve("A*")
			if type(current) == str:
				print current
				break




	def is_solution(self):
		'''

		'''
		for domain in self.domains:
			if len(self.domains[domain]) > 1:
				return False
		return True

	def get_neighbours(self):
		'''

		'''
		minlen = float("inf")
		current_domain = None
		neighbours = list()
		for domain in range(len(self.domains)):
			if len(self.domains[domain]) == 1:
				continue
			if (len(self.domains[domain])) < minlen:
				minlen = len(self.domains[domain])
				current_domain = domain

		for color in self.domains[current_domain]:
			neighbour = copy.deepcopy(self)
			neighbour.domains[current_domain] = [color]
			neighbour.domains = self.gac.rerun(neighbour.domains, current_domain)
			if not neighbour.is_illegal():
				neighbours.append(neighbour)
		self.neighbours = neighbours
		return neighbours

	def get_arc_cost(self):
		'''

		'''
		return 1

	def get_h(self):
		'''

		'''
		h = 0
		for domain in self.domains:
			h += len(self.domains[domain]) - 1
		self.h = h
		return self.h

	def is_illegal(self):
		'''

		'''
		for node in self.constraints:
			for edge in self.constraints[node]:
				if len(self.domains[node]) == 1 and len(self.domains[edge]) == 1 and self.domains[node] == self.domains[edge]:
					return True
		return False

	def __lt__(self, other):
		'''

		'''
		if self.f == other.f:
			return self.h < other.h
		return self.f < other.f

	def __eq__(self, other):
		'''

		'''
		return self.domains == other.domains


if __name__ == "__main__":
	b = Board("6.txt", 4)
	b.parse_text_file()
	vertexcoloring = probleminstance(b.constraint_dict, b.domain_dict)
