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
    
    def build(self, board, size):
        self.board = board
        self.size = size
        canvas_width = board.columns * size
        canvas_height = board.rows * size

        self.frame = tk.Frame(self, None)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                    width=canvas_width, height=canvas_height)
            
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
        self.canvas.pack()


    def drawPath(self, node):
        if node != self.board.startNode or node != self.board.endNode:
            self.drawRectangle(node, 'black')

    def clear(self):
        self.frame.pack_forget()
        self.frame.destroy()
        self.canvas.destroy()
        self.canvas = None
        self.frame = None
        

gui = None

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def solveAstar():
    current = astar.solve('A*')
    if current != False:
        gui.drawPath(current)
        gui.canvas.pack()
        root.after(1000, solveAstar)
    else:
        print("done")

def solveBFS():
    current = astar.solve('BFS')
    if current != False:
        gui.drawPath(current)
        gui.canvas.pack()
        root.after(100, solveBFS)
    else:
        print("done")

def solveDFS():
    current = astar.solve('DFS')
    if current != False:
        gui.drawPath(current)
        gui.canvas.pack()
        root.after(100, solveDFS)
    else:
        print("done")

def openBoard():
    filename = askopenfilename(parent=root)
    board = Board(filename)
    global gui
    if gui != None:
        gui.clear()

    gui = GUI(root)
    gui.build(board, 32)
    gui.pack(side="top", fill="both", expand="false")
    astar = Astar(board, gui)


def makeMenu(root):
        menubar = tk.Menu(root)
        boardmenu = tk.Menu(menubar, tearoff=0)
        boardmenu.add_command(label='Open file', command=openBoard)
        menubar.add_cascade(label='Board', menu=boardmenu)

        typemenu = tk.Menu(menubar, tearoff=0)
        typemenu.add_command(label='BFS', command=solveBFS)
        typemenu.add_command(label='DFS', command=solveDFS)
        typemenu.add_command(label='Best first', command=solveAstar)
        menubar.add_cascade(label='Type', menu=typemenu)

        root.config(menu=menubar)

if __name__ == "__main__":
    root = tk.Tk()
    makeMenu(root)
    board = Board('3.txt')
    gui = GUI(root)
    gui.build(board, 32)
    gui.pack(side="top", fill="both", expand="true")
    astar = Astar(board, gui)
    root.mainloop()


