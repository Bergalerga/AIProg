import Tkinter as tk

from Board import Board

class GUI(tk.Frame):
	'''
	Class responsible for drawing the user interface. Also contains rectangles.
	'''
	def __init__(self, parent, board):
		'''
		Initializes tkInter, and creates the canvas, in which additional widgets are created.
		'''
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.board = board
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=600, height=600)
		self.frame = tk.Frame(self, None)
		self.pack(fill="both", side="top")

	def build(self):
		'''

		'''
		center_width = self.canvas.winfo_reqwidth() / 2
		center_height = self.canvas.winfo_reqheight() / 2
		self.id_list = list()
		
		circle_size = 15
		for vertex in self.board.vertexes:
			x = vertex[1]
			y = vertex[2]
			self.id_list.append(self.canvas.create_oval(x * circle_size, 
														y * circle_size, 
														x * circle_size + 15, 
														y * circle_size + 15))
		for edge in self.board.edges:
			x1 = self.board.vertexes[edge[0]][1]
			y1 = self.board.vertexes[edge[0]][2]
			x2 = self.board.vertexes[edge[1]][1]
			y2 = self.board.vertexes[edge[1]][2]
			self.canvas.create_line(x1 * circle_size + 7.5,
									y1 * circle_size + 7.5,
									x2 * circle_size + 7.5,
									y2 * circle_size + 7.5)

		self.canvas.pack()

	def make_menu(self):
		'''
		Creates the menu at the top of the interface, allowing you to open boards
		from a file.
		'''
		menu_bar = tk.Menu(self.parent)
		board_menu = tk.Menu(menu_bar, tearoff=0)
		board_menu.add_command(label='Open file', command=self.open_menu)
		menu_bar.add_cascade(label='Board', menu=board_menu)

	def color_vertex(self, node, color='white'):
		'''
		Colors a given node with the color defined.
		'''
		circle_size = 15
		index_of_node = self.board.nodes.index(node)
		self.id_list[index_of_node] = self.canvas.create_oval(
									node.cartesian_x * circle_size,
									node.cartesian_y * circle_size,
									node.cartesian_x * circle_size + 15,
									node.cartesian_y * circle_size + 15,
									fill = color)

print("LOL")
if __name__ == "__main__":
	print("lol")
	b = Board("1.txt", 4)
	b.parse_text_file()
	gui = GUI(b, None)
	gui.build()
	gui.pack()
	vertexcoloring = probleminstance(b.constraint_dict, b.domain_dict)
	print("")
	gui.mainloop()

	

		

