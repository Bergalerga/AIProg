class GAC():
	def __init__(self, CSP):
		self.state = CSP
		self.revise_queue = []


	def initialize(self):
		for variable in self.state.variables:
			if variable in self.state.constraints:
				self.revise_queue.append((variable, self.state.constraints[variable]))

	def domain_filtering_loop(self):
		while self.revise_queue:
			revise_pair = self.revise_queue.pop(0)
			domain_reduced = self.revise(revise_pair)
			if domain_reduced:
				variable = revise_pair[0]
				for constraint in self.state.constraints[variable]:
					if len(self.state.domains[constraint]) != 1:
						self.revise_queue.append((constraint, self.state.constraints[constraint]))
		#print self.state.domains
		return self.state

	def revise(self, revise_pair):
		for neighbour_node in revise_pair[1]:
			if len(self.state.domains[neighbour_node]) == 1:
				if (self.state.domains[neighbour_node][0] in self.state.domains[revise_pair[0]]):
					#print "reduce"
					self.state.domains[revise_pair[0]].remove(self.state.domains[neighbour_node][0])
					return True
		return False

	def rerun(self):
		for variable in self.state.variables:
			if variable in self.state.constraints:
				self.revise_queue.append((variable, self.state.constraints[variable]))
		self.domain_filtering_loop()

		