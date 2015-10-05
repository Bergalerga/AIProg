import Tkinter as tk
from tkFileDialog import askopenfilename
import sys
from constraints import Constraints

from board import Board
from probleminstance import Probleminstance

class GUI(tk.Frame):
	'''
	Class responsible for drawing the user interface. Also contains rectangles.
	'''
	def __init__(self, parent):
		'''
		Initializes tkInter, and creates the canvas, in which additional widgets are created.
		'''
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=600, height=600)
		self.controller = Controller(self)
		self.id_list = list()

	def build(self, board):
		'''
		Builds the gui from a given board.
		'''
		self.board = board
		self.middle_x = self.canvas.winfo_reqwidth() / 2
		self.middle_y = self.canvas.winfo_reqheight() / 2
		self.x_multiplicative = self.middle_x / self.board.max_width
		self.y_multiplicative = self.middle_y / self.board.max_height
		self.id_list = list()
		self.circle_size = 10
		for vertex in self.board.vertexes:
			x = (vertex[1] * self.x_multiplicative) + (self.middle_x - self.circle_size)
			y = (vertex[2] * self.y_multiplicative) + (self.middle_y - self.circle_size)
			self.id_list.append(self.canvas.create_oval(x, y, x + 10, y + 10))
		
		for edge in self.board.edges:
			x1 = (self.board.vertexes[edge[0]][1] * self.x_multiplicative) + (self.middle_x - self.circle_size)
			y1 = (self.board.vertexes[edge[0]][2] * self.y_multiplicative) + (self.middle_y - self.circle_size)
			x2 = (self.board.vertexes[edge[1]][1] * self.x_multiplicative) + (self.middle_x - self.circle_size)
			y2 = (self.board.vertexes[edge[1]][2] * self.y_multiplicative) + (self.middle_y - self.circle_size)
			self.canvas.create_line(x1 + 5, y1 + 5, x2 + 5, y2 + 5)

		self.canvas.pack()

	def color_vertex(self, x, y, color='white'):
		'''
		Colors a given node with the color defined.
		'''
		x = (x * self.x_multiplicative) + (self.middle_x - self.circle_size)
		y = (y * self.y_multiplicative) + (self.middle_y - self.circle_size)
		self.canvas.create_oval(x, y, x + 10, y + 10, fill = color)

	def make_menu(self):
		'''
		Creates the menu at the top of the interface, allowing you to open boards
		from a file.
		'''
		menu_bar = tk.Menu(self.parent)
		board_menu = tk.Menu(menu_bar, tearoff=0)
		board_menu.add_command(label='Open file', command=self.controller.open_board)
		menu_bar.add_cascade(label='Board', menu=board_menu)

		k_menu = tk.Menu(menu_bar, tearoff=0)
		k_menu.add_command(label='2', command=lambda number='2': self.controller.solve(number))
		k_menu.add_command(label='3', command=lambda number='3': self.controller.solve(number))
		k_menu.add_command(label='4', command=lambda number='4': self.controller.solve(number))
		k_menu.add_command(label='5', command=lambda number='5': self.controller.solve(number))
		k_menu.add_command(label='6', command=lambda number='6': self.controller.solve(number))
		k_menu.add_command(label='7', command=lambda number='7': self.controller.solve(number))
		k_menu.add_command(label='8', command=lambda number='8': self.controller.solve(number))
		k_menu.add_command(label='9', command=lambda number='9': self.controller.solve(number))
		k_menu.add_command(label='10', command=lambda number='10': self.controller.solve(number))
		menu_bar.add_cascade(label="K", menu=k_menu)

		root.config(menu=menu_bar)

	def clear(self):
		self.canvas.delete("all")

class Controller:

	'''
	Class responsible for initializing a run, and drawing to the gui.
	'''
	def __init__(self, gui):
		'''
		Initializes with a gui.
		'''
		self.gui = gui
		self.K = 2
		self.colored = list()

	def reset(self):
		'''
		Resets the gui, preparing it for a new run.
		'''
		self.gui.clear()
		self.gui.build(self.board)
		self.colored = dict()

	def open_board(self):
		'''
		Opens a board when it is selected in the board menu.
		'''
		filename = askopenfilename(parent=root)
		self.board = Board(filename, self.K)
		self.board.parse_text_file()
		self.reset()
		gui.pack()

	def solve(self, number):
		'''
		Initializes a solve run, and calls the loop to solve.
		'''
		self.k = int(number)
		self.board.K = int(number)
		self.reset()
		self.board.make_domain_dict()
		self.board.make_constraint_dict()
		self.vc = Probleminstance(self.board.domain_dict, self.board.constraint_dict)
		self.vc.initialize()
		if self.vc.is_solution():
			self.color_vertexes(self.vc)
			return
		self.solve_loop()

	def solve_loop(self):
		'''
		Recursively calls one step of the algorithm at a time, coloring
		the gui for each time.
		'''
		solutions = self.vc.solve()
		problem_object = solutions[0]
		current = solutions[1]
		prev_current = solutions[2]
		if isinstance(current, Probleminstance):
			self.color_vertexes(current)
			root.after(refresh_time, self.solve_loop)
		else:
			print("------------------")
			if not prev_current.is_solution():
				print("Run terminated, the problem is not solvable")
				print("------------------")
			print(current)
			count = 0
			for domain in prev_current.domains:
				if len(prev_current.domains[domain]) > 1:
					count += 1
			print ("Variables without color assignment: " + str(count))
			self.color_vertexes(prev_current)


	def color_vertexes(self, current):
		'''
		Colors the vertexes that has a set color.
		'''
		for vertex in current.domains:
			if len(current.domains[vertex]) == 1:
				a = self.board.vertexes[vertex]
				num = current.domains[vertex][0]
				x = a[1]
				y = a[2]
				try:
					if self.colored[x, y] == num:
						continue
				except KeyError:
					self.colored[x, y] = num
				if num == 0:
					self.gui.color_vertex(x, y, 'blue')
				elif num == 1:
					self.gui.color_vertex(x, y, 'green')
				elif num == 2:
					self.gui.color_vertex(x, y, 'yellow')
				elif num == 3:
					self.gui.color_vertex(x, y, 'red')
				elif num == 4:
					self.gui.color_vertex(x, y, 'cadet blue')
				elif num == 5:
					self.gui.color_vertex(x, y, 'lemon chiffon')
				elif num == 6:
					self.gui.color_vertex(x, y, 'pink')
				elif num == 7:
					self.gui.color_vertex(x, y, 'dark khaki')
				elif num == 8:
					self.gui.color_vertex(x, y, 'chocolate')
				elif num == 9:
					self.gui.color_vertex(x, y, 'seashell2')
				else:
					self.gui.color_vertex(x, y, 'black')
				self.colored[x, y] = num

if __name__ == "__main__":
	global refresh_time
	refresh_time = 50
	if (len(sys.argv) == 2 and int(sys.argv[1])):
		refresh_time = sys.argv[1]
	root = tk.Tk()
	gui = GUI(root)
	gui.make_menu()
	gui.mainloop()