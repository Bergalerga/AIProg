from gac_nonogram import Gac_nonogram
from astar import Astar
from constraints import Constraints

import copy

class Probleminstance():
 	'''
 	Class holding a state of the problem, with domains and constraints. Also used to represent a node in astar.
 	'''


 	def __init__(self, domains, constraint_list):
 		'''
 		Initializes information, and sets the constraint formula.
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
		self.gac = Gac_nonogram()

	def initialize(self):
		'''
		Initializes, and runs the initial domain filtering loop.
		'''
		self.gac.initialize(self.domains, self.constraints)
		self.domains = self.gac.domain_filtering_loop()
		self.astar = Astar(self)
		

	def solve(self):
		'''
		Iteratively ran to find new states.
		'''
		self.current = self.astar.solve("A*")
		return [self.current, self.astar.prev_current]

	def is_solution(self):
		'''
		Returns true if this state is a solution state, false if not.
		'''
		for domain in self.domains:
			if len(self.domains[domain]) != 1:
				return False
		return True

	def get_neighbours(self):
		'''
		Returns the neighbours of this state.
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
		Returns the cost of moving from this state. Always 1 in this problem.
		'''
		return 1

	def get_h(self):
		'''
		Returns the h value, based on the amount of possible values for each row and column.
		'''
		h = 0
		for domain in self.domains:
			h += len(self.domains[domain])
		self.h = h
		return h

	def is_illegal(self):
		'''
		Returns true if this is a legal state, false if not.
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
		Less than comparison, compares on f primarily, h secondarily. Used by astar.
		'''
		if self.f == other.f:
			return self.h < other.h
		return self.f < other.f

	def __eq__(self, other):
		'''
		Equals operator, checks if the domains are equal.
		'''
		return self.domains == other.domains

	def __str__(self):
		'''
		String representation of this state's domains.
		'''
		return str(self.domains)