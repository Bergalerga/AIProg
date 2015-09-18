class Read():
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

	def __init__(self, file):
		file = open(file, 'r')
		self.fileData = file.readlines()
		file.close()

	def parseTextFile(self):
		verticesAndEdges = self.fileData[0].replace("\n", "").split(" ")
		self.numberOfVertices = int(verticesAndEdges[0])
		self.numberOfEdges = int(verticesAndEdges[1])
		self.vertexes = list()
		self.edges = list()
		fileIndex = 1
		while True:
			vertice = self.fileData[fileIndex].replace("\n", "").split(" ")
			if (len(vertice)) != 3:
				break
			self.vertexes.append([float(x) for x in vertice])
			fileIndex += 1
		while fileIndex < len(self.fileData):
			edge = self.fileData[fileIndex].replace("n", "").split(" ")
			if (len(edge)) != 2:
				break
			self.edges.append([int(x) for x in edge])
			fileIndex += 1

		print(self.numberOfVertices)
		print(self.numberOfEdges)
		print(self.vertexes)
		print(self.edges)

	def build(self):
		self.nodes = list()
		for vertex in self.vertexes:
			self.nodes.append(Node(int(vertex[0]), vertex[1], vertex[2]))



if __name__ == "__main__":
	f = Read("1.txt")
	f.parseTextFile()