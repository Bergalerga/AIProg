from node import Node
import heapq

class Astar():
    def __init__(self, board, gui):
        #trenger vi gui og board her, eller burde vi ikke ha det?
        self.gui = gui
        self.board = board
        self.opened = []
        self.closed = []
        heapq.heapify(self.opened)

    def solve(self):
        #Setting heuristic values for all nodes

        self.board.startNode.h = self.board.distanceToEndNode(self.board.startNode)
        self.board.startNode.f = self.board.startNode.g + self.board.startNode.h
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
            
            #Denne delen er jeg usikker paa om er riktig, passer vi paa aa oppdatere barns G ++? Pseudokoden i Keiths doc er litt annerledes
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






            



        
