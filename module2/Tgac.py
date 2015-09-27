class GAC():
	def __init__(self):
		state = None
		revise_queue = []

	def initialize(self, CSP):
		state = CSP
		for variable in state.variables:
			self.revise_queue.append((variable, state.constraints[variable]))

	def domain_filtering_loop(self):
		while self.revise_queue:
			revise_pair = self.revise_queue.pop(0)
			domain_reduced = self.revise(revise_pair)
			if domain_reduced:
				variable = revise_pair[0]
				for constraint in state.constraints[variable]:
					if len(state.domain[constraint]) != 1:
						self.revise_queue.append((constraint, state.constraints[constraint]))
		return state

	def revise(self, revise_pair):
		for neighbour_node in revise_pair[1]:
			if len(state.domain[neighbour_node]) == 1:
				if (state.domain[neighbour_node][0] in state.domain[revise_pair[0]]):
					state.domain[revise_pair[0]].remove(state.domain[neighbour_node][0])
					return True
		return False

	def rerun(self):
		pass