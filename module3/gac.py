from constraints import Constraints
class GAC:


	'''

	'''
	def initialize(self, domains = {}):
		'''

		'''
		self.constraints = Constraints.constraints
		self.domains = domains
		self.revise_queue = list()
		for node in self.constraints:
			for constraint in self.constraints[node]:
				self.revise_queue.append([node, constraint])
		
		

	def domain_filtering_loop(self):
		'''

		'''
		while self.revise_queue:
			node, constraint = self.revise_queue.pop(0)
			if self.revise(node, constraint):
				for constraint_edge in Constraints.get_edge(constraint):
					if [constraint, constraint_edge] not in self.revise_queue:
						self.revise_queue.append([constraint, constraint_edge])
		return self.domains

	def revise(self, node, constraint):
		'''

		'''
		if len(self.domains[constraint]) == 1:
			#Constraints.if_satisfies(node, constraint, domain)
			if self.domains[constraint][0] in self.domains[node]:
				self.domains[node].remove(self.domains[constraint][0])
				return True
		return False

	def rerun(self, domains = {}, focal_node = None):
		'''

		'''
		self.revise_queue = list()
		self.constraints = Constraints.constraints
		self.domains = domains
		for constraint in self.constraints[focal_node]:
			self.revise_queue.append([constraint, focal_node])
		self.domain_filtering_loop()
		return self.domains