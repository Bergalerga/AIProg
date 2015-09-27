from GUI import GUI

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

	def __init__(self, file):
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
		while True:
			vertice = self.file_data[file_index].replace("\n", "").split(" ")
			if (len(vertice)) != 3:
				break
			self.vertexes.append([float(x) for x in vertice])
			file_index += 1
		while file_index < len(self.file_data):
			edge = self.file_data[file_index].replace("n", "").split(" ")
			if (len(edge)) != 2:
				break
			self.edges.append([int(x) for x in edge])
			file_index += 1
		self.indexes = list()
		for vertex in self.vertexes:
			self.indexes.append(int(vertex[0]))
