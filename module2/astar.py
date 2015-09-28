from node import Node
import heapq

class Astar():
    '''
    The main algorithm, responsible for solving the pathfinding problem
    '''


    def __init__(self, node):
        '''
        Initializes the required components used by the algorithm, and a board to work with.
        '''
        self.startnode = node
        self.current = node
        self.opened = []
        self.closed = []
        self.current.f = self.current.g + self.current.get_h()
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
            if self.current.is_solution():
                return self.statistics()
            for neighbour in self.current.get_neighbours():
                if neighbour.is_illegal():
                    continue
                temporary_g = self.current.g + self.current.get_arc_cost()

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
            print(self.current.domains)
            return self.current

    def evaluate(self, child, predecessor):
        '''
        Evaluates and updates the g, h and f values for a given node, compared to another node.
        '''
        child.predecessor = predecessor
        child.g = predecessor.g + child.get_arc_cost()
        child.f = child.g + child.get_h()

    def propagate(self, predecessor):
        '''
        Iteratively evaluates a node compared to its predecessor, all the way to the start node.
        '''
        for child in predecessor.neighbours:
            if (predecessor.g+1) < child.g:
                child.predecessor = predecessor
                child.g = predecessor.g + child.get_arc_cost()
                child.f = child.g + child.get_h()
                self.propagate(child)

    def clear(self):
        '''
        Clears the values set by the algorithm, preparing it for a new run.
        '''
        self.current = self.startnode
        self.opened = []
        self.closed = []
        self.current.h = self.current.get_h()
        self.current.f = self.current.g + self.current.get_h()
        self.opened.append(self.current)

    def statistics(self):
        count = 0
        node = self.current
        while node.predecessor:
            count += 1
            node = node.predecessor
        return "Nodes generated: " + str(len(self.opened) + len(self.closed)) + " | Solution length: " + str(count)

