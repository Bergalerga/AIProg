import copy
import math
from Tgac import GAC

class CSPState():
	def __init__(self, variables, domains, constraints):
		#GAC relevant info
		self.variables = variables
		self.domains = domains
		self.constraints = constraints

		#A* relevant info
		self.h = 0
		self.f = 0
		self.g = 0
		self.predecessor = None
		self.neighbours = []

	#If all variables have been set, it is a solution and returns True
	def is_solution(self):
		for domain in self.domains:
			if len(self.domains[domain]) != 1:
				return False
		return True

	#Will create successornodes from current state
	def get_neighbours(self):
		minlen = float("inf")
		current_domain = None
		for domain in range(len(self.domains)):
			if len(self.domains[domain]) == 1:
				continue
			if len(self.domains[domain]) < minlen:
				minlen = len(self.domains[domain])
				current_domain = domain
		for color in self.domains[current_domain]:
			neighbour_state = copy.deepcopy(self)
			#gac = GAC(self, self.domains[current_domain])
			neighbour_state.domains[current_domain] = [color]
			self.neighbours.append(neighbour_state)
		return self.neighbours
		
	#Returns arc_cost, in this case it is always 1
	def get_arc_cost(self):
		return 1

	#Returns the heurestic distance to a solution, based on how large remaining domains are
	def get_h(self):
		h = 0
		for domain in range(len(self.domains)):
			h += len(self.domains[domain])
		return h

	def is_illegal(self):
		for key in self.constraints:
			for value in self.constraints[key]:	
				if len(self.domains[key]) == 1 and len(self.domains[value]) == 1 and (self.domains[key]) == (self.domains[value]):
					return True
		return False

	def __lt__(self, other):
		'''
		Method to compare two node object with respect to the f and h values. Used to sort the heap queue
		in the Astar algorithm.
		'''
		if self.f == other.f:
			return self.h < other.h
		return self.f < other.f

	def __eq__(self, other):
		'''

		'''
		return self.domains == other.domains
