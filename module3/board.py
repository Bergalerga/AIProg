from itertools import combinations, izip_longest
from probleminstance import Probleminstance

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
		self.rows_info.reverse()
		row_dict = self.make_domain_dict(self.row_length, self.rows_info, 1)
		column_dict = self.make_domain_dict(self.column_length, self.columns_info, 0)
		self.domain_dict = dict(row_dict.items() + column_dict.items())
		self.constraint_dict = {}
		self.make_constraint_dict(row_dict, column_dict)

	def make_domain_dict(self, size, info, num):
		'''

		'''
		temp_domain_dict = {}
		for node in range(size):
			length, block_length, number_of_blocks = self.get_free_spaces(size, info[node])
			free_spaces = length - block_length - (number_of_blocks -1)
			blocks = info[node]
			block_representation = list()

			#Get representation of block
			block_num = 0
			for block in blocks:
				block_num += 1
				if block_num > 1:
					block_repr = [0]
					nums = [1]*block
					block_repr.extend(nums)
				else:
					block_repr = [1]*block
				block_representation.append(block_repr)

			
			for space_placement in self.space_placement(free_spaces, number_of_blocks + 1):


				spaces_representation = list()
				for spaces in space_placement:
					space_repr = [0]*spaces
					spaces_representation.append(space_repr)
				zipped_list = izip_longest(spaces_representation, block_representation)

				domain = list()
				for zipitem in zipped_list:
					for lists in zipitem:
						if lists != None:
							domain.extend(lists)
				if (num, node) in temp_domain_dict:
					temp_domain_dict[(num, node)].append(domain)
				else:
					temp_domain_dict[(num, node)] = [domain]
		return temp_domain_dict

	def make_constraint_dict(self, row_dict, column_dict):
		'''

		'''
		for row_node in row_dict:
			for column_node in column_dict:
				if row_node in self.constraint_dict:
					self.constraint_dict[row_node].append(column_node)
				else:
					self.constraint_dict[row_node] = [column_node]
				if column_node in self.constraint_dict:
					self.constraint_dict[column_node].append(row_node)
				else:
					self.constraint_dict[column_node] = [row_node]



	def get_free_spaces(self, length, block_array):
		'''

		'''
		block_length = 0
		number_of_blocks = 0
		for block in block_array:
			number_of_blocks += 1
			block_length += block
		return length, block_length, number_of_blocks

	def space_placement(self, spaces, length):
		'''

		'''
		for c in combinations(range(spaces + length - 1), length - 1):
			yield tuple(b - a - 1 for a, b in zip((-1,) + c, c + (spaces + length - 1,)))


if __name__ == "__main__":
	board = Board("tale.txt")
	board.parse_text_file()
	pr = Probleminstance(board.domain_dict, board.constraint_dict)

	pr.initialize()
	while isinstance(pr, Probleminstance):
		pr = pr.solve()
