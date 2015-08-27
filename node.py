class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 0
        self.g = 0
        self.f = 0
        self.predecessor = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
    	return "X: " + str(self.x) + " Y: " + str(self.y)

    def __repr__(self):
    	return "X: " + str(self.x) + " Y: " + str(self.y)
    