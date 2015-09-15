from node import Node
import heapq

class Astar():
    def __init__(self, board, gui):
        self.gui = gui
        self.board = board
        self.opened = []
        self.closed = []
        self.current = self.board.startNode
        self.board.startNode.h = self.board.distanceToEndNode(self.board.startNode)
        self.board.startNode.f = self.board.startNode.g + self.board.startNode.h
        self.opened.append(self.current)
        self.prev_current = None

    def setHValues(self):
        return

    def solve(self, mode):

        
        if mode == 'A*':
            heapq.heapify(self.opened)   
        
        if (len(self.opened)):
            self.prev_current = self.current
            if mode == 'A*':
                self.current = heapq.heappop(self.opened)
            elif mode =='DFS':
                self.current = self.opened.pop(-1)
            else:
                self.current = self.opened.pop(0)            
            self.closed.append(self.current)
            if self.current == self.board.endNode:
                return False
            neighbours = self.board.getNeighbours(self.current)
            
            for neighbour in neighbours:
                self.current.children.append(neighbour)

                if self.board.isUnwalkable(neighbour):
                    continue

                temporary_g = self.current.g + 1

                if neighbour not in self.opened and neighbour not in self.closed:

                    self.evaluate(neighbour, self.current)
                    if mode == 'A*':
                        heapq.heappush(self.opened, neighbour)
                    else:
                        self.opened.append(neighbour)
                    #self.drawNode(neighbour, 'violet')
                elif temporary_g < neighbour.g:
                    self.evaluate(neighbour, self.current)
                    if neighbour in self.closed:
                        self.propagate(neighbour)
            #print [self.opened[x].h for x in range(len(self.opened))]
            return self.current

    def evaluate(self, child, predecessor):
        child.predecessor = predecessor
        child.g = predecessor.g + 1
        child.h = self.board.distanceToEndNode(child)
        child.f = child.g + child.h

    def propagate(self, predecessor):
        for child in predecessor.children:
            if (predecessor.g+1) < child.g:
                child.predecessor = predecessor
                child.g = predecessor.g +1
                child.h = self.board.distanceToEndNode(child)
                child.f = child.g + child.h
                propagate(child)

    def clear(self):
        self.opened = []
        self.closed = []
        self.current = self.board.startNode
        self.board.startNode.h = self.board.distanceToEndNode(self.board.startNode)
        self.board.startNode.f = self.board.startNode.g + self.board.startNode.h
        self.opened.append(self.current)






            



        
