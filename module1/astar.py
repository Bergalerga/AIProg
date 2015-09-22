from node import Node
import heapq

class Astar():
    '''
    The main algorithm, responsible for solving the pathfinding problem
    '''


    def __init__(self, nodes):
        '''
        Initializes the required components used by the algorithm, and a board to work with.
        '''
        self.nodes = nodes
        self.opened = []
        self.closed = []
        for nodes in self.nodes:
            for node in nodes:
                if node.startnode == True:
                    self.startnode = node
                    self.current = self.startnode
                elif node.endnode:
                    self.endnode = node
        self.startnode.h = self.startnode.distance_to_node(self.endnode)
        self.startnode.f = self.startnode.g + self.startnode.h
        self.opened.append(self.current)
        self.prev_current = None

    def solve(self, mode):
        '''
        This is the agenda loop. It will return the next node chosen. Has a parameter mode, which
        defines which algorithm to perform.
        '''
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
            if self.current.isSolution():
                return False
            neighbours = self.getNeighbours(self.current)
            
            for neighbour in neighbours:
                self.current.children.append(neighbour)

                if neighbour.unwalkable:
                    continue

                temporary_g = self.current.g + self.current.get_arc_cost(neighbour)

                if neighbour not in self.opened and neighbour not in self.closed:

                    self.evaluate(neighbour, self.current)
                    if mode == 'A*':
                        heapq.heappush(self.opened, neighbour)
                    else:
                        self.opened.append(neighbour)
                elif temporary_g < neighbour.g:
                    self.evaluate(neighbour, self.current)
                    if neighbour in self.closed:
                       self.propagate(neighbour)
            return self.current

    def evaluate(self, child, predecessor):
        '''
        Evaluates and updates the g, h and f values for a given node, compared to another node.
        '''
        child.predecessor = predecessor
        child.g = predecessor.g + 1
        child.h = child.distance_to_node(self.endnode)
        child.f = child.g + child.h

    def propagate(self, predecessor):
        '''
        Iteratively evaluates a node compared to its predecessor, all the way to the start node.
        '''
        for child in predecessor.children:
            if (predecessor.g+1) < child.g:
                child.predecessor = predecessor
                child.g = predecessor.g +1
                child.h = child.distance_to_node(self.endnode)
                child.f = child.g + child.h
                self.propagate(child)

    def getNeighbours(self, node):
        '''
        Return the vertical and horizontal neighbours of the given node.
        '''
        nodes = list()
        if node.x < len(self.nodes) - 1:
            nodes.append(self.nodes[node.x + 1][node.y])
        if node.y < len(self.nodes[0]) - 1:
            nodes.append(self.nodes[node.x][node.y + 1])
        if node.x > 0:
            nodes.append(self.nodes[node.x - 1][node.y])
        if node.y > 0:
            nodes.append(self.nodes[node.x][node.y - 1])
        return nodes

    def clear(self):
        '''
        Clears the values set by the algorithm, preparing it for a new run.
        '''
        self.opened = []
        self.closed = []
        for nodes in self.nodes:
            for node in nodes:
                if node.startnode == True:
                    self.startnode = node
                    self.current = self.startnode
                elif node.endnode:
                    self.endnode = node
        self.startnode.h = self.startnode.distance_to_node(self.endnode)
        self.startnode.f = self.startnode.g + self.startnode.h
        self.opened.append(self.current)
