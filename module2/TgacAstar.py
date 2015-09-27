from Tboard import Board
from TCSPState import CSPState
from astar import Astar
from Tgac import GAC

class gacAstar():

	def __init__(self):
		csp_problem = None

	def solve(self):
		board = Board('testen.txt')
		board.parse_text_file()
		domains = self.make_domain_dict(board.indexes, 3)
		constraints = self.make_constraint_dict(board.edges)
		csp_state = CSPState(board.indexes, domains, board.edges)
		gac = GAC(csp_state)
		gac.initialize()
		new_state = gac.domain_filtering_loop()
		astar = Astar(new_state)
		while not new_state.is_solution():
			new_state = astar.solve('A*')
			gac = GAC(new_state)
			gac.initialize()
			new_state = gac.domain_filtering_loop()
			


	def make_domain_dict(self, variables, K):
		domains = {}
		for variable in variables:
			for color in range(K):
				if variable in domains:
					domains[variable].append(color)
				else:
					domains[variable] = [color]
		return domains

	def make_constraint_dict(self, edges):
		constraints = {}
		for edge in edges:
			if edge[0] in constraints:
				constraints[edge[0]].append(edge[1])
			else:
				constraints[edge[0]] = [edge[1]]
		return constraints

test = gacAstar()
test.solve()