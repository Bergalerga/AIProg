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
        boardSize = fileData[0].rstrip().split(" ")
        self.rows = int(boardSize[0])
        self.columns = int(boardSize[1])

        startAndStop = fileData[1].rstrip().split(" ")
        unWalkableAreas = []
        for elements in fileData[2:]:
            unWalkable = elements.rstrip().split(" ")
            area = [int(x) for x in unWalkable]
            unWalkableAreas.append(area)
        self.nodes = list()
        for x in range(self.rows):
            y_list = list()
            for y in range(self.columns):

                if x == int(startAndStop[0]) and y == int(startAndStop[1]):
                    self.startnode = Node(x, y, startnode=True)
                    y_list.append(self.startnode)
                elif x == int(startAndStop[2]) and y == int(startAndStop[3]):
                    self.endnode = Node(x, y, endnode=True)
                    y_list.append(self.endnode)
                else:
                    y_list.append(Node(x, y))
                for elements in unWalkableAreas:
                    if x >= elements[0] and y >= elements[1]:
                        if x <= elements[0] + (elements[2] - 1) and y <= elements[1] +(elements[3] - 1):
                            y_list[y].illegal=True

            self.nodes.append(y_list)

        for nodes in self.nodes:
            for node in nodes:
                #Sets h value for the node.
                distance = math.fabs(node.x - self.endnode.x)
                distance += math.fabs(node.y - self.endnode.y)
                node.h = distance
                #Generates the neighours of the node.
                neighbours = list()
                if node.x < self.rows - 1:
                    neighbours.append(self.nodes[node.x + 1][node.y])
                if node.y < self.columns - 1:
                    neighbours.append(self.nodes[node.x][node.y + 1])
                if node.x > 0:
                    neighbours.append(self.nodes[node.x - 1][node.y])
                if node.y > 0:
                    neighbours.append(self.nodes[node.x][node.y - 1])
                node.neighbours = neighbours

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

    def getArcCost(self, node):
        return 1

    def isSolution(self, node):
        if node == self.endNode:
            return True
        return False

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
        self.width = 600
        self.height = 600
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=self.width, height=self.height)
        self.id_list = list()

    def build(self, board):
        '''
        Builds the GUI from a given board, and packing it in the end.
        '''
        self.board = board
        #TODO
        if self.width > self.height:
            self.size = self.width / board.rows
        else:
            self.size = self.height / board.columns

        self.frame = tk.Frame(self, None)
        self.frame.grid(column=0, row=0)

        for width in reversed(range(board.rows)):
            for height in range(board.columns):
                top = (board.columns - height - 1) * self.size
                left = width * self.size
                bottom = top + self.size
                right = left + self.size

                if (board.nodes[width][height].startnode):
                    fill = 'green'
                elif (board.nodes[width][height].endnode):
                    fill = 'grey'
                elif (board.nodes[width][height].illegal):
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
        self.id_list.append(self.canvas.create_rectangle(left, top, right, bottom, fill = fill))

    def drawPath(self, node, color):
        '''
        Given a node, the method will draw the full path of all the nodes where this node 
        came from, all the way back to the start node.
        '''
        for item in self.id_list:
            self.canvas.delete(item)
        while node.predecessor:
            if node != self.board.startnode or node != self.board.endnode:
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
        self.gui.build(self.board)
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
        if isinstance(current, Node):
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveAstar)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')
            print(current)


    def solveBFS(self):
        '''
        Starts astar, and rund through in breadth-first mode
        '''
        current = self.astar.solve('BFS')
        if isinstance(current, Node):
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveBFS)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')
            print(current)

    def solveDFS(self):
        '''
        Starts astar, and runs through in Depth-first mode
        '''
        current = self.astar.solve('DFS')
        if isinstance(current, Node):
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(current, 'black')
            root.after(refreshTime, self.solveDFS)
        else:
            self.gui.drawPath(self.astar.prev_current, 'pink')
            self.gui.drawPath(self.astar.current, 'black')
            print(current)

    def openBoard(self):
        '''
        Opens the file system, allowing you to select a board. It then builds a board based on whats selected.
        '''
        filename = askopenfilename(parent=root)
        self.board = Board(filename)    
        self.gui.clear()
        self.gui.build(self.board)
        gui.pack(side="top", fill="both", expand="false")  
        self.astar = Astar(self.board.startnode)

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
