class Node():
    def __init__(self, x, y):
        #Koordinat
        self.x = x
        self.y = y
        #Heurestikk, Avstand fra start, total beregnet avstand
        self.h = 0
        self.g = 0
        self.f = 0
        #Beste forelder
        self.predecessor = None
        #Alle barn/naboer
        self.children = []

    # For aa sortere heapq
    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    # For aa sjekke om to noder er like
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    #Returnerer x og y koordinat for noden representert som en String
    def __str__(self):
    	return "X: " + str(self.x) + " Y: " + str(self.y)

    def __repr__(self):
    	return "X: " + str(self.x) + " Y: " + str(self.y)
    