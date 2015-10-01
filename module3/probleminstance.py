 rom gac import GAC
from astar import Astar
from constraints import Constraints

import copy

class Probleminstance():
 	'''

 	'''
 	def __init__(self, domains = {} ):
 		'''

 		'''
 		#A* INFO
		self.h = 0
		self.g = 0
		self.f = 0
		self.predecessor = None
		self.neighbours = []

		#GAC INFO
		self.constraints = Constraints.constraints
		self.domains = domains

		#init gac
		self.gac = GAC()

		def initialize(self):
		'''

		'''

		self.gac.initialize(self.domains)
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
		pass

	def get_arc_cost(self):
		'''

		'''
		return 1

	def get_h(self):
		'''

		'''
		pass

	def is_illegal(self):
		'''

		'''
		pass

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