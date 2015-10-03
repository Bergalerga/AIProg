class GAC:
	'''

	'''
	def initialize(self, domains = {}, constraints = None):
		'''

		'''
		self.constraints = constraints
		self.domains = domains
		self.revise_queue = list()
		for node in self.constraints.involved:
			for constraint_edge in self.constraints.involved[node]:
				self.revise_queue.append([node, constraint_edge])

	def domain_filtering_loop(self):
		'''

		'''
		while self.revise_queue:
			node, constraint_node = self.revise_queue.pop(0)
			if self.revise(node, constraint_node):
				for edges in self.constraints.involved[node]:
					if [edges, node] not in self.revise_queue:
						self.revise_queue.append([edges, node])
						

		return self.domains

	def revise(self, node, constraint_node):
		'''
		node repr med tall 0, constraint repr som lambdafunksjon.
		'''
		revised = False
		for x_domain in self.domains[node]:
			satisfies = 0
			for y_domain in self.domains[constraint_node]:
				x_index = node[1]
				y_index = constraint_node[1]
				if self.constraints.expression(x_domain, y_domain, x_index, y_index):
					satisfies += 1
			if satisfies == 0:
				self.domains[node].remove(x_domain)
				revised = True
		return revised

	def rerun(self, domains = {}, focal_node = None, constraints = None):
		'''

		'''
		self.revise_queue = list()
		self.domains = domains
		self.constraints = constraints
		for constraint_edge in self.constraints.involved[focal_node]:
			self.revise_queue.append([constraint_edge, focal_node])
		self.domain_filtering_loop()
