from node import Node
from state import State
from gac import GAC
from astar import Astar

class VertexColoring():
	def __init__(self, board, k):
		self.startState = State(board, k)
		self.startState = self.startState.parse_text_file()

	def solve(self):
		gac = GAC()
		gac.initialize(self.startState)
		newState = gac.domain_filtering()
		if !isSolution(newState):
			#Initialize a* med 
			astar = Astar()





	def isSolution(self, state):
		return False




'''
	def solve(self):
		if state is not solution or not wrong:
			Continue normal A∗ s e a r c h ( with S0 i n the r o o t node ) by :
			− Popping s e a r c h nodes from the agenda
			− Gene r a tin g t h e i r s u c c e s s o r s t a t e s ( by making a s sump ti on s )
			− E n f o r ci n g the assumption i n each s u c c e s s o r s t a t e by r e d u ci n g
			the domain o f the assumed v a r i a b l e t o a s i n g l e t o n s e t
			− C alli n g GAC−Rerun on each newly−g e n e r a t e d s t a t e
			− Computing the f , g and h v al u e s f o r each new s t a t e ,
			where h i s based on the s t a t e o f the CSP
			a f t e r the c a l l t o GAC−Rerun .'''






if __name__ == "__main__":
    vc = VertexColoring(board, 4)
    vc.solve()

