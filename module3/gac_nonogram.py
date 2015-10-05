from gac import GAC

class Gac_nonogram(GAC):
	'''
	Specialization/Subclass of the GAC algorithm.
	'''

	def __init__(self):
		'''
		Initializes the general GAC.
		'''
		GAC.__init__(self)

	def revise(self, node, constraint_node):
		'''
		Specialized revise function used for this problem.
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
