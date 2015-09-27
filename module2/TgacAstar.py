from Tboard import Board
from TCSPState import CSPState
from astar import Astar
from Tgac import GAC

class gacAstar():

	def __init__(self):
		csp_problem = None

	def solve(self):
		board = Board('1.txt')
		board.parse_text_file()
		domains = make_domain_dict(board.indexes, 4)
		constraints = make_constraint_dict(board.edges)
		csp_state = CSPState(board.indexes, domains, constraints)
		while !csp_state.is_solution:
			gac = GAC(csp_state)
			gac.initialize()
			gac.domain_filtering_loop()


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