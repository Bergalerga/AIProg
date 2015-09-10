from node import Node
import heapq

class Astar():
    def __init__(self, board, gui):
        #trenger vi gui og board her, eller burde vi ikke ha det?
        self.gui = gui
        self.board = board
        self.opened = []
        self.closed = []
        

    def solveAstar(self):

        self.board.startNode.h = self.board.distanceToEndNode(self.board.startNode)
        self.board.startNode.f = self.board.startNode.g + self.board.startNode.h
        heapq.heapify(self.opened)
        heapq.heappush(self.opened, (self.board.startNode.f, self.board.startNode.h, self.board.startNode))
        
        while (len(self.opened)):
            current = heapq.heappop(self.opened)[2]
            self.closed.append(current)
            if current == self.board.endNode:
                if self.gui == None:
                    self.printPath(current.predecessor)
                else:
                    self.drawPath(current.predecessor, 'purple')
                break
            neighbours = self.board.getNeighbours(current)
            
            for neighbour in neighbours:
                current.children.append(neighbour)

                if self.board.isUnwalkable(neighbour):
                    continue

                temporary_g = current.g + 1

                if (neighbour.f, neighbour.h, neighbour) not in self.opened and neighbour not in self.closed:
                    self.evaluate(neighbour, current)
                    heapq.heappush(self.opened, (neighbour.f, neighbour.h, neighbour))
                    self.drawNode(neighbour, 'violet')
                elif temporary_g < neighbour.g:
                    self.evaluate(neighbour, current)
                    if neighbour in self.closed:
                        self.propagate(neighbour)    


    def evaluate(self, child, predecessor):
        child.predecessor = predecessor
        child.g = predecessor.g + 1
        child.f = child.g + self.board.distanceToEndNode(child)

    def propagate(self, predecessor):
        for child in predecessor.children:
            if (predecessor.g+1) < child.g:
                child.predecessor = predecessor
                child.g = predecessor.g +1
                child.f = child.g + child.h
                propagate(child)

    def solveBFS(self):
        start = self.board.startNode
        self.opened.append(start)
        while True:
            current = self.opened.pop(0)
            print(self.opened)
            self.closed.append(current)

            if current == self.board.endNode:
                self.drawPath(current, 'purple')
                break

            neighbours = self.board.getNeighbours(current)
            for neighbour in neighbours:
                if self.board.isUnwalkable(neighbour):
                    continue
                if neighbour not in self.closed and neighbour not in self.opened:
                    self.opened.append(neighbour)
                    neighbour.predecessor = current
                    self.drawNode(neighbour, 'violet')

    def solveDFS(self):
        start = self.board.startNode
        self.opened.append(start)
        while True:
            current = self.opened.pop(-1)
            self.closed.append(current)

            if current == self.board.endNode:
                self.drawPath(current, 'purple')
                break

            neighbours = self.board.getNeighbours(current)
            for neighbour in neighbours:
                if self.board.isUnwalkable(neighbour):
                    continue
                if neighbour not in self.opened and neighbour not in self.closed:
                    self.opened.append(neighbour)
                    neighbour.predecessor = current
                    self.drawNode(neighbour, 'violet')

    def printPath(self, node):
        path = list()
        while True:
            if node.predecessor != None:
                path.append(node)
                node = node.predecessor
            else:
                break
        print(path)

    def drawPath(self, node, fill):

        while True:
            if node.predecessor:
                self.gui.drawRectangle(node, fill)
                node = node.predecessor
            else:
                break

    def drawNode(self, node, fill):
        self.gui.drawRectangle(node, fill)






            



        
