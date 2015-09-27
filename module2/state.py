from node import Node

class State():
	'''
	self.numberOfVertices = the number of vertices in the graph
	self.numberOfEdges = the number of edges in the graph
	self.vertexes = 2-dimensional list. For each vertex, [0] denotes the index, [1] the x coord 
	and [2] the y coord. Values are all type float
	self.
	self.edges = 2-dimensional list. For each edge, [0] denotes the index of the first vertice,
	[1] denotes the second vertex.
	self.nodes = list of node objects containing the edges.
	'''

	def __init__(self, file, K):
		file = open(file, 'r')
		self.file_data = file.readlines()
		file.close()
		self.K = K
		for node in self.nodes:
			node.add_domain(K)

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
		'''
		print(self.number_of_vertices)
		print(self.number_of_edges)
		print(self.vertexes)
		print(self.edges)
		'''
		self.nodes = list()
		for vertex in self.vertexes:
			self.nodes.append(Node(int(vertex[0]), vertex[1], vertex[2], 4))
		for edge in self.edges:
			self.nodes[edge[0]].edges.append(self.nodes[edge[1]])
			self.nodes[edge[1]].edges.append(self.nodes[edge[0]])

		self.startNode = self.nodes[0]

	def distanceToEndNode(self):
		h = 0
		for node in self.nodes:
			h += (len(node.domain)-1)
		return h

	def getNeighbours(self, node):
		return node.edges

	def getArcCost(self, node):
		return 1

	def isSolution(self, node):
		pass

