import Tkinter as tk
from tkFileDialog import askopenfilename
import sys

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

	def build(self, board):
		'''

		'''
		self.board = board

		center_width = self.canvas.winfo_reqwidth()
		center_height = self.canvas.winfo_reqheight()
		self.id_list = list()
		
		self.circle_size = 10
		for vertex in self.board.vertexes:
			x = (vertex[1] / self.board.max_width) * (center_width - self.circle_size)
			y = (vertex[2] / self.board.max_height) * (center_height - self.circle_size)
			#x = vertex[1]
			#y = vertex[2]
			print(x)
			print(y)

			self.id_list.append(self.canvas.create_oval(x, 
														y, 
														x + 10, 
														y + 10))
		for edge in self.board.edges:
			x1 = self.board.vertexes[edge[0]][1]
			y1 = self.board.vertexes[edge[0]][2]
			x2 = self.board.vertexes[edge[1]][1]
			y2 = self.board.vertexes[edge[1]][2]
			self.canvas.create_line(x1 + 5,
									y1 + 5,
									x2 + 5,
									y2 + 5)

		self.canvas.pack()

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

	def color_vertex(self, x, y, color='white'):
		'''
		Colors a given node with the color defined.
		'''

		self.canvas.create_oval(x * self.circle_size,
								y * self.circle_size,
								x * self.circle_size + 10,
								y * self.circle_size + 10,
								fill = color)


	def clear(self):
		self.canvas.delete("all")

class Controller:

	'''

	'''
	def __init__(self, gui):
		'''

		'''
		self.gui = gui
		self.K = 2

	def reset(self):
		'''

		'''
		self.gui.clear()
		self.gui.build(self.board)

	def open_board(self):
		'''

		'''
		filename = askopenfilename(parent=root)
		self.board = Board(filename, self.K)
		self.board.parse_text_file()
		self.reset()
		gui.pack()

	def solve(self, number):
		'''

		'''
		self.k = int(number)
		self.board.K = int(number)
		self.board.make_domain_dict()
		self.reset()
		self.vc = Probleminstance(self.board.constraint_dict, self.board.domain_dict)
		self.solve_loop()

	def solve_loop(self):
		'''

		'''
		solutions = self.vc.solve()
		current = solutions[0]
		prev_current = solutions[1]
		if isinstance(current, Probleminstance):
			self.color_vertexes(current)
			root.after(refresh_time, self.solve_loop)
		else:
			self.color_vertexes(prev_current)

	def color_vertexes(self, current):
		'''

		'''
		for vertex in current.domains:
				if len(current.domains[vertex]) == 1:
					a = self.board.vertexes[vertex]
					num = current.domains[vertex][0]
					x = a[1]
					y = a[2]
					if num == 0:
						self.gui.color_vertex(x, y, 'blue')
					elif num == 1:
						self.gui.color_vertex(x, y, 'green')
					elif num == 2:
						self.gui.color_vertex(x, y, 'yellow')
					elif num == 3:
						self.gui.color_vertex(x, y, 'red')
					else:
						self.gui.color_vertex(x, y, 'purple')

if __name__ == "__main__":
	global refresh_time
	refresh_time = 50
	if (len(sys.argv) == 2 and int(sys.argv[1])):
		refresh_time = sys.argv[1]
	root = tk.Tk()
	gui = GUI(root)
	gui.make_menu()
	gui.mainloop()






	

		

