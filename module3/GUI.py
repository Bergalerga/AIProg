from board import Board
from probleminstance import Probleminstance

import Tkinter as tk
from tkFileDialog import askopenfilename
import sys

class GUI(tk.Frame):
	'''
	Class responsible for drawing the graphical interface, and the steps of the algorithm.
	'''


	def __init__(self, parent):
		'''
		Initializes tkinter, and the guis controller.
		'''
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.width = 600
		self.height = 600
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=self.width, height=self.height)
		self.controller = Controller(self)
		self.id_list = list()

	def build(self, board):
		'''
		Builds a graphial representation of a given board.
		'''
		self.board = board
		self.rows = self.board.number_of_columns
		self.columns = self.board.number_of_rows
		if self.rows > self.columns:
			self.square_size = (self.width / self.rows) / 1.5
		else:
			self.square_size = (self.height / self.columns) / 1.5
		for row in reversed(range(self.rows)):
			for column in range(self.columns):
				x1 = row * self.square_size
				y1 = column * self.square_size
				x2 = row * self.square_size + self.square_size
				y2 = column * self.square_size + self.square_size
				self.canvas.create_rectangle(x1, y1, x2, y2)
		
		draw_start_x = (self.square_size * self.rows) + self.square_size
		draw_start_y = (self.square_size * self.columns) + self.square_size
		x_count = 0
		y_count = self.square_size / 2
		for row in self.board.rows_info:
			for num in row:
				self.canvas.create_text(draw_start_x + x_count, y_count, text=str(num))
				x_count += 20
			y_count += self.square_size
			x_count = 0

		x_count = self.square_size / 2
		y_count = 0
		for column in self.board.columns_info:
			for num in column:
				self.canvas.create_text(x_count, draw_start_y + y_count, text=str(num))
				y_count += 20
			y_count = 0
			x_count += self.square_size
		
		self.canvas.pack()

	def draw_square(self, x, y, num):
		'''
		Draws a square from its x and y coordinates, with the given color.
		'''
		x1 = x * self.square_size
		y1 = y * self.square_size
		x2 = x1 + self.square_size
		y2 = y1 + self.square_size
		if num == 1:
			self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue')
		else:
			self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')			

	def make_menu(self):
		'''
		Creates a menu, allowing you to select a board.
		'''
		menu_bar = tk.Menu(self.parent)
		board_menu = tk.Menu(menu_bar, tearoff=0)
		board_menu.add_command(label='Open file', command=self.controller.open_board)
		menu_bar.add_cascade(label='Board', menu=board_menu)

		go_menu = tk.Menu(menu_bar, tearoff=0)
		go_menu.add_command(label='Go', command=self.controller.solve)
		menu_bar.add_cascade(label='Run', menu=go_menu)

		root.config(menu=menu_bar)

	def clear(self):
		'''
		Clears the canvas by deleting all of its elements.
		'''
		self.canvas.delete("all")


class Controller():
	'''
	Class responsible for controlling the algorithm, and updates the gui.
	'''


	def __init__(self, gui):
		'''
		Initializes the controller with a gui
		'''
		self.gui = gui

	def open_board(self):
		'''
		Opens the board selected from the file menu, and prepares for a new run.
		'''
		filename = askopenfilename(parent=root)
		self.board = Board(filename)
		self.board.parse_text_file()
		self.reset()
		gui.pack()

	def reset(self):
		'''
		Resets the gui and builds a new board.
		'''
		self.gui.clear()
		self.gui.build(self.board)
		self.board.parse_text_file()

	def solve(self):
		'''
		Starts the algorithm.
		'''
		self.reset()
		self.problem = Probleminstance(self.board.domain_dict, self.board.constraint_dict)
		self.problem.initialize()
		if self.problem.is_solution():
			self.color_vertexes(self.problem)
		self.solve_loop()

	def solve_loop(self):
		'''
		Iteratively solves the problem, printing steps each time.
		'''
		solutions = self.problem.solve()
		current = solutions[0]
		prev_current = solutions[1]
		if isinstance(current, Probleminstance):
			root.after(refresh_time, self.solve_loop)
		else:
			print("---------------")
			if not prev_current.is_solution():
				print("Run terminated, the problem is not solvable")
				print("------------------")
			print(current)
			self.color_vertexes(prev_current)

	def color_vertexes(self, current):
		'''
		Colors all of the vertexes.
		'''
		for domain in current.domains:
			if len(current.domains[domain]) == 1 and domain[0] == 0:
				for index in range(len(current.domains[domain][0])):
					self.gui.draw_square(domain[1], index, current.domains[domain][0][index])

if __name__ == "__main__":
	global refresh_time
	refresh_time = 0
	if (len(sys.argv) == 2 and int(sys.argv[1])):
		refresh_time = sys.argv[1]
	root = tk.Tk()
	gui = GUI(root)
	gui.make_menu()
	gui.mainloop()
	