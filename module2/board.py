from math import fabs

class Board():
	

	'''
	self.numberOfVertices = the number of vertices in the graph
	self.numberOfEdges = the number of edges in the graph
	self.vertexes = 2-dimensional list. For each vertex, [0] denotes the index, [1] the x coord 
	and [2] the y coord. Values are all type float
	self.
	self.edges = 2-dimensional list. For each edge, [0] denotes the index of the first vertice,
	[1] denotes the second vertex.
	self.variables = list of variable objects containing the edges.
	'''
	def __init__(self, file, K):
		self.K = K
		file = open(file, 'r')
		self.file_data = file.readlines()
		file.close()

	def parse_text_file(self):
		'''

		'''
		vertices_and_edges = self.file_data[0].replace("\n", "").split(" ")
		self.number_of_vertices = int(vertices_and_edges[0])
		self.number_of_edges = int(vertices_and_edges[1])
		self.vertexes = list()
		self.edges = list()
		file_index = 1
		self.max_width = 0
		self.max_height = 0
		while True:
			vertice = self.file_data[file_index].rstrip("\n").rstrip(" ").split(" ")
			if (len(vertice)) != 3:
				break
			self.vertexes.append([float(x) for x in vertice])
			if fabs(float(vertice[1])) > self.max_width:
				self.max_width = fabs(float(vertice[1]))
			if fabs(float(vertice[2])) > self.max_height:
				self.max_height = fabs(float(vertice[2]))
			file_index += 1
		while file_index < len(self.file_data):
			edge = self.file_data[file_index].rstrip("\n").rstrip(" ").split(" ")
			if (len(edge)) != 2:
				break
			self.edges.append([int(x) for x in edge])
			file_index += 1
		self.indexes = list()
		for vertex in self.vertexes:
			self.indexes.append(int(vertex[0]))

		self.make_domain_dict()
		self.make_constraint_dict()

	def make_domain_dict(self):
		self.domain_dict = {}
		for node in self.indexes:
			self.domain_dict[node] = list()
			for color in range(self.K):
				self.domain_dict[node].append(color)


	def make_constraint_dict(self):
		self.constraint_dict = {}
		for node in self.indexes:
			self.constraint_dict[node] = list()
		for first_node, second_node in self.edges:
			self.constraint_dict[first_node].append(second_node)
			self.constraint_dict[second_node].append(first_node)
		

