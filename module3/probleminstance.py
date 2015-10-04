from gac import GAC
from astar import Astar
from constraints import Constraints

import copy

class Probleminstance():
 	'''

 	'''
 	def __init__(self, domains, constraint_list):
 		'''

 		'''
 		#A* INFO
		self.h = 0
		self.g = 0
		self.f = 0
		self.predecessor = None
		self.neighbours = []

		#GAC INFO
		self.constraints = Constraints("column[y_index] == row[x_index]", ["column", "row", "x_index", "y_index"], constraint_list)
		self.domains = domains

		#init gac
		self.gac = GAC()

	def initialize(self):
		'''

		'''
		self.gac.initialize(self.domains, self.constraints)
		self.domains = self.gac.domain_filtering_loop()
		self.astar = Astar(self)
		

	def solve(self):
		'''

		'''
		self.current = self.astar.solve("A*")
		return [self.current, self.astar.prev_current]

	def is_solution(self):
		'''

		'''
		for domain in self.domains:
			if len(self.domains[domain]) != 1:
				return False
		return True

	def get_neighbours(self):
		'''

		'''
		minlen = float("inf")
		current_domain = None
		neighbours = list()
		for domain in self.domains:
			if len(self.domains[domain]) == 1:
				continue
			if (len(self.domains[domain])) < minlen:
				minlen = len(self.domains[domain])
				current_domain = domain
		for variation in self.domains[current_domain]:
			copy_domains = copy.deepcopy(self.domains)
			copy_domains[current_domain] = [variation]
			copy_domains = self.gac.rerun(copy_domains, current_domain, self.constraints)
			pi = Probleminstance(copy_domains, self.constraints.involved)
			neighbours.append(pi)
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
			h += len(self.domains[domain])
		self.h = h
		return h

	def is_illegal(self):
		'''

		'''
		for node in self.domains:
			if self.domains[node] == []:
				return True
			for constraint_node in self.constraints.involved[node]:
				legal = False
				for x_domain in self.domains[node]:
					for y_domain in self.domains[constraint_node]:
						x_index = node[1]
						y_index = constraint_node[1]
						if self.constraints.expression(x_domain, y_domain, x_index, y_index):
							legal = True
				if legal == False:
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

	def __str__(self):
		'''

		'''
		return str(self.domains)