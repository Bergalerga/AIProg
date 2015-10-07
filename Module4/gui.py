import Tkinter as tk
import sys
import random

from solver import Solver

class GUI(tk.Frame):
	'''

	'''

	def __init__(self, parent):
		'''

		'''
		tk.Frame.__init__(self, parent)
		self.rows = 4
		self.cols = 4
		self.parent = parent
		self.width = 600
		self.height = 600
		self.rectangle_size = 150
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=self.width, height=self.height)
		self.id_list = list()

	def build(self):
		'''

		'''
		self.board = list()
		x1 = random.randint(0, 3)
		x2 = random.randint(0, 3)
		y1 = random.randint(0, 3)
		y2 = random.randint(0, 3)
		while x1 == x2 and y1 == y2:
			x2 = random.randint(0, 4)
			y2 = random.randint(0, 4)
		for x in range(self.rows):
			y_list = list()
			for y in range(self.cols):
				if x == x1 and y == y1:
					y_list.append(2)
				elif x == x2 and y == y2:
					y_list.append(2)
				else:
					y_list.append(0)
			self.board.append(y_list)
		self.color_state(self.board)
		self.canvas.pack()

	def color_state(self, state):
		'''

		'''
		print(self.board)
		self.delete_items()
		for x in range(len(self.board)):
			for y in range(len(self.board)):
				x1 = x * self.rectangle_size
				y1 = y * self.rectangle_size
				x2 = x1 + self.rectangle_size
				y2 = y1 + self.rectangle_size
				number = self.board[x][y]
				if number == 0:
					fill = 'white'
				elif number == 2:
					fill = 'PaleVioletRed1'
				elif number == 4:
					fill = 'PaleVioletRed2'
				elif number == 8:
					fill = 'maroon1'
				elif number == 16:
					fill = 'maroon2'
				elif number == 32:
					fill = 'maroon3'
				elif number == 64:
					fill = 'maroon4'
				elif number == 128:
					fill = 'red'
				elif number == 256:
					fill = 'red2'
				elif number == 512:
					fill = 'red3'
				elif number == 1024:
					fill = 'red4'
				else:
					fill = 'black'
				self.id_list.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill))

	def delete_items(self):
		'''

		'''
		for item in self.id_list:
			self.canvas.delete(item)

	def init_controller(self):
		'''

		'''
		self.controller = Controller(self)

class Controller():
	'''

	'''


	def __init__(self, gui):
		'''

		'''
		solver = Solver()
		

	def solve(self):
		'''

		'''
		solver = solver.solve()
		while not solver.is_solution():
			root.after(refresh_time, solve)


if __name__ == "__main__":
    '''
    Initializes TkInter, and passes it to the gui, and initializes the gui's menu and controller. 
    Sets an iteration delay of Astar, if defined from command line input. Iteration delay defaults to 50 ms.
    '''
    global refresh_time
    refresh_time = 50
    if (len(sys.argv) == 2 and int(sys.argv[1])):
        refresh_time = sys.argv[1]
    root = tk.Tk()
    gui = GUI(root)
    gui.build()
    gui.init_controller()
    gui.pack()
    root.mainloop()


