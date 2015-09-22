from board import Board
from astar import Astar

class GAC():
    '''
    The General Arc-Consistency Algorithm
    '''
    def __init__(self, board, K):
        self.board = board
        self.K = K
        for node in self.board.nodes:
            node.add_domain(K)
        board.startNode.domain = [1]

    def solve(self):
        self.initialize()
        for node in self.board.nodes:
            if len(node.domain) == 0:
                return False
            #if len(node.domain) > 1:
            #    node = self.search()
            #    self.rerun(node)


    def initialize(self):
        #need to fill up queue with focalvariable-constraint pairs
        self.revise_queue = []
        for node in self.board.nodes:
            self.revise_queue.append((node, node.edges))

        self.domain_filtering()

    def domain_filtering(self):
        while self.revise_queue:
            revise_pair = self.revise_queue.pop(0)
            domain_reduced = self.revise(revise_pair)
            if domain_reduced:
                node = revise_pair[0]
                for edge in node.edges:
                    if len(edge.domain) != 1:
                        self.revise_queue.append((edge, edge.edges))
        self.debug_print()

    def revise(self, revise_pair):
        for edge in revise_pair[1]:
            if len(edge.domain) == 1:
                print(edge.domain)
                print(revise_pair[0].domain)
                if (edge.domain[0] in revise_pair[0].domain):
                    revise_pair[0].domain.remove(edge.domain[0])
                    return True
        return False

    def search(self):
        astar = Astar(self.board)
        while astar != False:
            astar = astar.solve('A*')
        return prev_current

    def rerun(self, node):
        for edge in node.edges:
            self.revise_queue.append((edge, edge.edges))
        self.domain_filtering()

    def debug_print(self):
        print("---------")

        for node in self.board.nodes:
            print([node, node.domain])
'''
    def makefunc(var_names, expression, envir=globals()):
        args = ""
        for n in var_names:
            args = args + " ," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")", envir)
'''

    

if __name__ == "__main__":
    board = Board("1.txt")
    board.parse_text_file()
    gac = GAC(board, 4)
    gac.solve()

