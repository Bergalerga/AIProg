class Variable():
	'''

	'''


	def __init__(self, index, cartesian_x, cartesian_y, domain):
		'''

		'''
		self.index = index
		self.cartesian_x = cartesian_x
		self.cartesian_y = cartesian_y
		self.domain = list()
		self.set_variable = None
		self.constraints = list()

	def add_domain(self, K):
		for color in range(K):
			self.domain.append(color)

	def remove_from_domain(self, value):
		self.domain.remove(value)

	def set_variable(self, value):
		self.set_variable = value

	def add_constraint(self, constraint)
		self.constraints.append(constraint)

	def __str__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)

	def __repr__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)