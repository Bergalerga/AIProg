from board import Board

class GAC():
    '''
    The General Arc-Consistency Algorithm
    '''
    def __init__(self, board, K):
        self.board = board
        self.K = K
        for node in self.board.nodes:
            node.add_domain(K)

    def solve(self):
        self.initialize()
        #if not solution:(tomt domene paa en node)
        #    astar search


    def initialize(self):
        #need to fill up queue with focalvariable-constraint pairs
        self.revise_queue = []
        for node in self.board.nodes:
            self.revise_queue.append((node, node.edges))

        self.domain_filtering(self.revise_queue)

    def domain_filtering(self, revise_queue):
        while revise_queue:
            revise_pair = self.revise_queue.pop(0)
            domain_reduced = self.revise(revise_pair)
            if domain_reduced:
                node = revise_pair[0]
                for edge in node.edges:
                    if len(edge.domain) != 1:
                        self.revise_queue.append((edge, edge.edges))

    def revise(self, revise_pair):
        for edge in revise_pair[1]:
            if len(edge.domain) == 1:
                revise_pair[0].domain.remove(edge.domain[0])
                return True
        return False

'''
    def rerun():
        for all constraints where X appears:
            self.revise_queue.push(pairs)
        domain_filtering()

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

