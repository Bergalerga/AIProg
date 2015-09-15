import Tkinter as tk
import heapq
import sys
import re
import math
from astar import Astar
from node import Node
from threading import Thread
from tkFileDialog import askopenfilename
import time

'''
(35, 25)
(3, 12) (21, 3)
(5, 4, 16, 1)
(5, 20, 16, 1)
(21, 5, 1, 16)

'''
class Board():

    '''
    Builds a board with a specified size for each rectangle. Requires the board to have
    a startnode, endnode, rows and columns. It also requires the isUnwalkable method, for any
    spaces that cannot be passed.
    '''
    def __init__(self, filename):
        board = open(filename, 'r')
        fileData = board.readlines()
        board.close()
        self.parseTextFile(fileData)

    def parseTextFile(self, fileData):
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
        for elements in self.unWalkableAreas:
            if node.x >= elements[0] and node.y >= elements[1]:
                if node.x <= elements[0] + (elements[2] - 1) and node.y <= elements[1] +(elements[3] - 1):                        return True
        return False

    def distanceToEndNode(self, node):
        distance = math.fabs(node.x - self.endNode.x)
        distance += math.fabs(node.y - self.endNode.y)
        return int(distance) 

    def getNeighbours(self, node):
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
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=600, height=600)
        self.controller = Controller(self)

    def build(self, board, size):
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
        x = node.x
        y = board.columns - node.y

        top = (y - 1) * self.size
        left = x * self.size
        bottom = top + self.size
        right = left + self.size
        #print "draw at %s, %s, %s, %s" % (left, top, right, bottom)
        self.canvas.create_rectangle(left, top, right, bottom, fill = fill)
        #self.canvas.pack()


    def drawPath(self, node, color):
        print("-----------")
        while node.predecessor:
            if node != self.board.startNode or node != self.board.endNode:
                self.drawRectangle(node, color)
                print(node)
                node = node.predecessor


    def makeMenu(self):
        menubar = tk.Menu(root)
        boardmenu = tk.Menu(menubar, tearoff=0)
        boardmenu.add_command(label='Open file', command=openBoard)
        menubar.add_cascade(label='Board', menu=boardmenu)

        typemenu = tk.Menu(menubar, tearoff=0)
        typemenu.add_command(label='BFS', command=lambda alg='bfs': self.controller.solve(alg))
        typemenu.add_command(label='DFS', command=lambda alg='dfs': self.controller.solve(alg))
        typemenu.add_command(label='Best first', command=lambda alg='best-first': self.controller.solve(alg))
        menubar.add_cascade(label='Type', menu=typemenu)

        root.config(menu=menubar)


    def clear(self):
        self.canvas.delete("all")     


class Controller(object):
    """

    """

    def __init__(self, gui=None):
        """
        Constructor
        """

        self.gui = gui
        self.flags = {'first_run': True}

    def solve(self, alg='best-first'):
        self.reset()
        astar.clear()
        self.gui.build(board, 16)
        if alg == 'best-first':
            self.solveAstar()
        elif alg == 'bfs':
            self.solveBFS()
        else: 
            self.solveDFS()

    def reset(self):
        self.gui.clear()
        astar.clear()

    def solveAstar(self):
        current = astar.solve('A*')
        if current != False:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(current, 'black')
            root.after(50, self.solveAstar)
        else:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(astar.current, 'black')

    def solveBFS(self):
        current = astar.solve('BFS')
        if current != False:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(current, 'black')
            root.after(50, self.solveBFS)
        else:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(astar.current, 'black')

    def solveDFS(self):
        current = astar.solve('DFS')
        if current != False:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(current, 'black')
            root.after(50, self.solveDFS)
        else:
            gui.drawPath(astar.prev_current, 'pink')
            gui.drawPath(astar.current, 'black')

def openBoard():
    
    global board
    global astar
    global gui

    filename = askopenfilename(parent=root)
    board = Board(filename)    
    if gui == None:
        gui = GUI(root)
    if gui != None:
        gui.clear()
    gui.build(board, 16)
    gui.pack(side="top", fill="both", expand="false")
    
    astar = Astar(board, gui)

if __name__ == "__main__":
    global gui
    root = tk.Tk()
    gui = GUI(root)
    gui.makeMenu()
    root.mainloop()


