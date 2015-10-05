class GAC(object):
	'''
	General GAC algorithm, used to filter out revise domains.
	'''
	def __init__(self):
		'''

		'''

	def initialize(self, domains = {}, constraints = None):
		'''
		Initializes constraints and domains. Runs an initial domain filtering loop.
		'''
		self.constraints = constraints
		self.domains = domains
		self.revise_queue = list()
		for node in self.constraints.involved:
			for constraint_edge in self.constraints.involved[node]:
				self.revise_queue.append([node, constraint_edge])

	def domain_filtering_loop(self):
		'''
		Goes through the edges to be revised, and removes illegal domains.
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
		Checks if a domain satisfies constraints, removing it if it does not. Returns True
		if something has been revised, False otherwise.
		'''
		revised = False
		for x_domain in self.domains[node]:
			satisfies = 0
			for y_domain in self.domains[constraint_node]:
				if self.constraints.expression(x_domain, y_domain):
					satisfies += 1
			if satisfies == 0:
				self.domains[node].remove(x_domain)
				revised = True

		return revised

	def rerun(self, domains = {}, focal_node = None, constraints = None):
		'''
		Reruns domain filtering loop on a specified node.
		'''
		self.revise_queue = list()
		self.domains = domains
		self.constraints = constraints
		for constraint_node in self.constraints.involved[focal_node]:
			self.revise_queue.append([constraint_node, focal_node])
		self.domain_filtering_loop()
		return self.domains