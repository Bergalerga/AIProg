
class Board():
	'''

	'''

	def __init__(self, file):
		file = open(file, 'r')
		self.file_data = file.readlines()
		file.close()

	def parse_text_file(self):
		'''

		'''
		dimensions = self.file_data[0].replace("\n", "").split(" ")
		self.row_length = int(dimensions[0])
		self.column_length = int(dimensions[1])
		self.rows_info = list()
		self.columns_info = list()
		file_index = 1
		while True:
			row = self.file_data[file_index].replace("\n", "").split(" ")
			self.rows_info.append([int(x) for x in row])
			file_index += 1
			if file_index > self.row_length:
				break
		while file_index < len(self.file_data):
			column = self.file_data[file_index].replace("\n", "").split(" ")
			self.columns_info.append([int(x) for x in column])
			file_index += 1
		self.make_domain_dict()

	def make_domain_dict(self):
		self.domain_dict = {}
		for node in range(self.row_length):
			number_of_spaces = -1
			total_block_length = 0
			for block_length in self.rows_info[node]:
				number_of_spaces += 1
				total_block_length += block_length
			places_to_put_space = self.row_length - total_block_length - number_of_spaces

			print node, self.rows_info[node], number_of_spaces, total_block_length, places_to_put_space

	def make_constraints():
		pass




if __name__ == "__main__":
	board = Board("1.txt")
	board.parse_text_file()