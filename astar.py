from node import Node
import heapq

class Astar():
    def __init__(self, board, gui):
        self.gui = gui
        self.board = board
        self.opened = []
        self.closed = []
        heapq.heapify(self.opened)

    def solve(self):
        #Setting heuristic values for all nodes

        self.board.startNode.f = self.board.distanceToEndNode(self.board.startNode)
        heapq.heappush(self.opened, (self.board.startNode.f, self.board.startNode))
        
        while (len(self.opened)):
            current = heapq.heappop(self.opened)[1]
            if current == self.board.endNode:
                if self.gui == None:
                    self.printPath(current.predecessor)
                else:
                    print(self.opened)
                    self.drawPath(current.predecessor, 'purple')
                break
            self.closed.append(current)
            neighbours = self.board.getNeighbours(current)
            for neighbour in neighbours:
                if neighbour in self.closed:
                    continue
                if self.board.isUnwalkable(neighbour):
                    continue

                temporary_g = current.g + 1

                if (neighbour.f, neighbour) not in self.opened or temporary_g < neighbour.g:
                    neighbour.predecessor = current
                    neighbour.g = temporary_g
                    neighbour.f = neighbour.g + self.board.distanceToEndNode(neighbour)
                    if (neighbour.f, neighbour) not in self.opened:
                        heapq.heappush(self.opened, (neighbour.f, neighbour))

    
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
        #for node in self.closed:
        #    self.gui.drawRectangle(node, 'violet')
        #for x,y in self.opened:
        #    self.gui.drawRectangle(y, 'violet')
        while True:
            if node.predecessor != None:
                self.gui.drawRectangle(node, fill)
                node = node.predecessor
            else:
                break

    def drawNode(self, node, fill):
        self.gui.drawRectangle(node, fill)






            



        
