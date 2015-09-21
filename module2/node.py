class Node():
	'''

	'''


	def __init__(self, index, cartesian_x, cartesian_y):
		'''

		'''
		self.index = index
		self.cartesian_x = cartesian_x
		self.cartesian_y = cartesian_y
		self.edges = list()
		self.domain = []

	def __str__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)

	def __repr__(self):
		return str(self.index) + " - " + str(self.cartesian_x) + " - " + str(self.cartesian_y)