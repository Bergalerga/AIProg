from board import Board

import Tkinter as tk
from tkFileDialog import askopenfilename
import sys

class GUI(tk.Frame):
	'''

	'''


	def __init__(self, parent):
		'''

		'''
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=600, height=600)
		self.controller = Controller(self)
		self.id_list = list()

	def build(self, board):
		'''

		'''
		self.board = board
		self.square_size = 15
		self.rows = self.board.row_length
		self.columns = self.board.column_length
		for row in range(self.rows):
			for column in range(self.columns):
				x1 = row * self.square_size
				y1 = column * self.square_size
				x2 = row * self.square_size + self.square_size
				y2 = column * self.square_size + self.square_size
				self.canvas.create_rectangle(x1, y1, x2, y2)
		self.canvas.pack()

	def make_menu(self):
		'''

		'''
		menu_bar = tk.Menu(self.parent)
		board_menu = tk.Menu(menu_bar, tearoff=0)
		board_menu.add_command(label='Open file', command=self.controller.open_board)
		menu_bar.add_cascade(label='Board', menu=board_menu)

		root.config(menu=menu_bar)

	def color_node(self):
		'''

		'''
		pass

	def clear(self):
		self.canvas.delete("all")


class Controller():
	'''

	'''


	def __init__(self, gui):
		'''

		'''
		self.gui = gui

	def open_board(self):
		'''

		'''
		filename = askopenfilename(parent=root)
		self.board = Board(filename)
		self.board.parse_text_file()
		self.reset()
		gui.pack()

	def reset(self):
		'''

		'''
		self.gui.clear()
		self.gui.build(self.board)

	def solve(self):
		'''

		'''
		pass

if __name__ == "__main__":
	global refresh_time
	refresh_time = 50
	if (len(sys.argv) == 2 and int(sys.argv[1])):
		refresh_time = sys.argv[1]
	root = tk.Tk()
	gui = GUI(root)
	gui.make_menu()
	gui.mainloop()
	