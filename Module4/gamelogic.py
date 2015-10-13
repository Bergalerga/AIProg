import random
import copy

class Gamelogic():
	'''

	'''

	def __init__(self):
		'''

		'''

	def move(self, direction, board):
		'''

		'''
		self.board = board
		copy_board = copy.deepcopy(self.board)
		if direction == 'RIGHT':
			self.move_right()
		
		elif direction == 'LEFT':
			self.move_left()

		elif direction == 'UP':
			self.move_up()

		elif direction == 'DOWN':
			self.move_down()

		if copy_board != self.board:
			self.board = self.append_random_number(self.board)
		return self.board

	def check_move(self, direction, board):
		self.board = board
		copy_board = copy.deepcopy(self.board)
		if direction == 'RIGHT':
			self.move_right()
		
		elif direction == 'LEFT':
			self.move_left()

		elif direction == 'UP':
			self.move_up()

		elif direction == 'DOWN':
			self.move_down()
		if self.board == copy_board:
			return None
		return self.board

	def move_up(self):
		'''

		'''
		self.reverse_board()
		self.move_left()
		self.reverse_board()

	def move_down(self):
		'''

		'''
		self.reverse_board()
		self.move_right()
		self.reverse_board()

	def move_left(self):
		'''

		'''
		moved = False
		for row in self.board:
			self.push('LEFT', row)
			for number in range(len(row) - 1):
				if row[number] != 0 and row[number] == row[number + 1]:
					row[number] += row[number]
					row[number + 1] = 0
					moved = True
					row = self.push('LEFT', row)
		return moved

	def move_right(self):
		'''

		'''
		moved = False
		for row in self.board:
			self.push('RIGHT', row)
			for number in reversed(range(len(row) - 1)):
				if row[number] != 0 and row[number] == row[number + 1]:
					row[number] += row[number]
					row[number + 1] = 0
					moved = True
					row = self.push('RIGHT', row)
		return moved

	def push(self, direction, row):
		'''

		'''
		for x in range(3):
			if direction == 'RIGHT':
				for number in range(0, 3):
					if row[number + 1] == 0:
						row[number + 1] = row[number]
						row[number] = 0
			elif direction == 'LEFT':
				for number in reversed(range(1, 4)):
					if row[number - 1] == 0:
						row[number - 1] = row[number]
						row[number] = 0
		return row

	def reverse_board(self):
		'''

		'''
		temp_board = list()
		for number in range(4):
			temp_board.append([self.board[count][number] for count in range(4)])
		self.board = temp_board

	def append_random_number(self, board):
		'''

		'''
		four_or_two = random.randint(1, 10)
		if four_or_two == 1:
			number = 4
		else:
			number = 2
		x_loc = random.randint(0, 3)
		y_loc = random.randint(0, 3)
		while board[x_loc][y_loc] != 0:
			x_loc = random.randint(0, 3)
			y_loc = random.randint(0, 3)
		board[x_loc][y_loc] = number
		return board

	def append_all_random_numbers(self, board):
		'''

		'''
		print("RANDOM NUMBERS")
		permutations = dict()
		permutations[2] = list()
		permutations[4] = list()
		for row in range(len(board)):
			for value in range(len(board)):
				if board[row][value] == 0:
					board[row][value] = 2
					permutations[2].append(copy.deepcopy(board))
					board[row][value] = 4
					permutations[4].append(copy.deepcopy(board))
					board[row][value] = 0
		print("RANDOM NUMBERS DONE")
		return permutations


	def is_solution(self, board):
		'''

		'''
		for row in board:
			if 2048 in row:
				return True
		return False

