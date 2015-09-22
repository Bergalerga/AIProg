class Node():
	'''

	'''


	def __init__(self, index, cartesian_x, cartesian_y, domain):
		'''

		'''
		self.index = index
		self.cartesian_x = cartesian_x
		self.cartesian_y = cartesian_y
		self.edges = list()
		self.domain = list()
		self.temporary_chosen = None
		self.h = 0
		self.g = 0
		self.f = 0

	def add_domain(self, K):
		for color in range(K):
			self.domain.append(color)

	def __str__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)

	def __repr__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)