import Tkinter as tk

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
    	for node in self.board.nodes:
    		self.id_list.append(self.canvas.create_oval(node.cartesian_x * circle_size,
    								node.cartesian_y * circle_size,
    								node.cartesian_x * circle_size + 15,
    								node.cartesian_y * circle_size + 15))
    		for edge in node.edges:
    			print(edge.cartesian_x)
    			self.canvas.create_line(node.cartesian_x * circle_size + 7.5,
    									node.cartesian_y * circle_size + 7.5,
    									edge.cartesian_x * circle_size + 7.5,
    									edge.cartesian_y * circle_size + 7.5)

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

    

    	

