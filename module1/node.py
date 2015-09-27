import math

class Node():
    '''
    Nodes held by the board, used to represent a square on the board.
    '''


    def __init__(self, x, y, unwalkable = False, startnode = False, endnode = False):
        '''
        Initializes the Node object, setting the given coordinates, and sets h, g and f values to 0.
        It also initializes the predecessor of the node, and a list of children.
        '''
        self.x = x
        self.y = y
        self.h = 0
        self.g = 0
        self.f = 0
        self.predecessor = None
        self.neighbours = []
        self.unwalkable = unwalkable
        self.startnode = startnode
        self.endnode = endnode

    def get_arc_cost(self, other):
        return 1

    def get_neighbours(self):
        return self.neighbours

    def get_h(self):
        return self.h

    def distance_to_node(self, other):
        distance = math.fabs(self.x - other.x)
        distance += math.fabs(self.y - other.y)
        return int(distance) 

    def is_solution(self):
        return self.endnode
    
    def __lt__(self, other):
        '''
        Method to compare two node object with respect to the f and h values. Used to sort the heap queue
        in the Astar algorithm.
        '''
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __eq__(self, other):
        '''
        Compares the nodes on equality. Used to check whether a node is the endNode or not.
        '''
        return self.x == other.x and self.y == other.y
    
    #Returnerer x og y koordinat for noden representert som en String
    def __str__(self):
        '''
        Prints a string representation of the node object, in the form of its x and y coordinates.
        '''
    	return "X: " + str(self.x) + " Y: " + str(self.y)

    def __repr__(self):
        '''
        Allows you to print node object in a collection. 
        '''
    	return "X: " + str(self.x) + " Y: " + str(self.y) + str([self.unwalkable, self.startnode, self.endnode])
    
