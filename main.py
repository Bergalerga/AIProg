import Tkinter as tk
from tkFileDialog import askopenfilename

from astar import Astar
from node import Node

import heapq
import sys
import re
import math


class Board():
    '''
    Responsible for the board that the gui and astar needs.
    '''


    def __init__(self, filename):
        '''
        Initializes the board by reading the given file name. Also calls the method to parse the textfile.
        '''
        board = open(filename, 'r')
        fileData = board.readlines()
        board.close()
        self.parseTextFile(fileData)

    def parseTextFile(self, fileData):
        '''
        Parses the textfile into a 2-dimensional list, containing nodes for each space in the board.
        '''
        boardSize = fileData[0].replace("(","").replace(")","").rstrip().split(",")
        self.rows = int(boardSize[0])
        self.columns = int(boardSize[1])

        startAndStop = re.findall(r'[^,;\s]+', fileData[1].replace("(", "").replace(")", ""))
        self.startNode = Node(int(startAndStop[0]), int(startAndStop[1]))
        self.endNode = Node(int(startAndStop[2]), int(startAndStop[3]))

        self.unWalkableAreas = []
        for elements in fileData[2:]:
            unWalkable = elements.replace("(","").replace(")","").rstrip().split(",")
            area = [int(x) for x in unWalkable]
            self.unWalkableAreas.append(area)
        
        self.nodes = list()
        for y in range(self.columns):
            x_list = list()
            for x in range(self.rows):
                x_list.append(Node(x, y))
            self.nodes.append(x_list)

    def isUnwalkable(self, node):
        '''
        Given a node, returns a boolean saying whether or not the node is possible to access, or if it's an obstacle.
        '''
        for elements in self.unWalkableAreas:
            if node.x >= elements[0] and node.y >= elements[1]:
                if node.x <= elements[0] + (elements[2] - 1) and node.y <= elements[1] +(elements[3] - 1):                        return True
        return False

    def distanceToEndNode(self, node):
        '''
        Return the manhattan distance from the current node to the end node.
        '''
        distance = math.fabs(node.x - self.endNode.x)
        distance += math.fabs(node.y - self.endNode.y)
        return int(distance) 

    def getNeighbours(self, node):
        '''
        Return the vertical and horizontal neighbours of the given node.
        '''
        nodes = []
        if node.x < self.columns - 1: 
            nodes.append(Node(node.x + 1, node.y))
        if node.y > 0:
            nodes.append(Node(node.x, node.y - 1))
        if node.x > 0:
            nodes.append(Node(node.x - 1, node.y))
        if node.y < self.rows - 1:
            nodes.append(Node(node.x, node.y + 1))
        return nodes

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

    def build(self, board, size):
        '''
        Builds the GUI from a given board, and packing it in the end.
        '''
        self.board = board
        self.size = size

        self.frame = tk.Frame(self, None)
        self.frame.grid(column=0, row=0)
        
            
        for width in reversed(range(board.rows)):
            for height in (range(board.columns)):
                top = (board.columns - height - 1) * size
                left = width * size
                bottom = top + size
                right = left + size

                if (board.startNode.x == width and board.startNode.y == height):
                    fill = 'green'
                elif (board.endNode.x == width and board.endNode.y == height):
                    fill = 'grey'
                elif (board.isUnwalkable(Node(width, height))):
                    fill = 'red'
                else: 
                    fill = 'white'
     
                self.canvas.create_rectangle(left, top, right, bottom, fill=fill)

        self.canvas.pack()

    def drawRectangle(self, node, fill):
        '''
        Given a node, the method will draw a rectangle on the canvas corresponding to the x 
        and y coordinates of the node.
        '''
        x = node.x
        y = self.board.columns - node.y

        top = (y - 1) * self.size
        left = x * self.size
        bottom = top + self.size
        right = left + self.size
        self.canvas.create_rectangle(left, top, right, bottom, fill = fill)

    def drawPath(self, node, color):
        '''
        Given a node, the method will draw the full path of all the nodes where this node 
        came from, all the way back to the start node.
        '''
        while node.predecessor:
            if node != self.board.startNode or node != self.board.endNode:
                self.drawRectangle(node, color)
                node = node.predecessor


    def makeMenu(self):
        '''
        Creates the menu at the top of the user interface. It also defines the actions to be 
        performed when the menu items are clicked.
        '''
        menubar = tk.Menu(root)
        boardmenu = tk.Menu(menubar, tearoff=0)
        boardmenu.add_command(label='Open file', command=self.controller.openBoard)
        menubar.add_cascade(label='Board', menu=boardmenu)

        typemenu = tk.Menu(menubar, tearoff=0)
        typemenu.add_command(label='BFS', command=lambda alg='bfs': self.controller.solve(alg))
        typemenu.add_command(label='DFS', command=lambda alg='dfs': self.controller.solve(alg))
        typemenu.add_command(label='Best first', command=lambda alg='best-first': self.controller.solve(alg))
        menubar.add_cascade(label='Type', menu=typemenu)

        root.config(menu=menubar)


    def clear(self):
        '''
        Clears the canvas, and deletes all the elements.
        '''
        self.canvas.delete("all") 

    def initController(self):
        '''
        Initializes the controller used by the GUI.
        '''
        self.controller = Controller(self)    


class Controller(object):
    """
    Responsible for handling events triggered by the user interface.
    """


    def __init__(self, gui):
        """
        Constructor, sets the instance of the user interface.
        """
        self.gui = gui

    
    def solve(self, alg='best-first'):
        '''
        Method triggered by selecting an algorithm from the user interface. 
        It will trigger the method corresponding to the algorithm, or default 
        to best first.
        '''
        self.reset()
        self.gui.build(self.board, 16)
        if alg == 'best-first':
            self.solveAstar()
        elif alg == 'bfs':
            self.solveBFS()
        else: 
            self.solveDFS()

    def reset(self):
        '''
        Resets the gui and the instance of astar, allowing a new run to be started.
        '''
        self.gui.clear()
        self.astar.clear()

    def solveAstar(self):
        ''' 
        Starts astar, and runs through in best-first mode
        '''
        current = self.astar.solve('A*')
        if current != False:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveAstar)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')

    def solveBFS(self):
        '''
        Starts astar, and rund through in breadth-first mode
        '''
        current = self.astar.solve('BFS')
        if current != False:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveBFS)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')

    def solveDFS(self):
        '''
        Starts astar, and runs through in Depth-first mode
        '''
        current = self.astar.solve('DFS')
        if current != False:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveDFS)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')

    def openBoard(self):
        '''
        Opens the file system, allowing you to select a board. It then builds a board based on whats selected.
        '''
        filename = askopenfilename(parent=root)
        self.board = Board(filename)    
        self.gui.clear()
        self.gui.build(self.board, 16)
        gui.pack(side="top", fill="both", expand="false")  
        self.astar = Astar(self.board)

if __name__ == "__main__":
    '''
    Initializes TkInter, and passes it to the gui, and initializes the gui's menu and controller. It also handles command line input.
    '''
    global refreshTime
    refreshTime = 50
    if (len(sys.argv) == 2 and int(sys.argv[1])):
        refreshTime = sys.argv[1]
    root = tk.Tk()
    gui = GUI(root)
    gui.initController()    
    gui.makeMenu()
    root.mainloop()


