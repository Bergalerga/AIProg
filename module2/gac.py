class GAC():
    '''
    The General Arc-Consistency Algorithm
    '''

    def __init__(self):
        self.revise_queue = []
        self.variables = []
        self.domain = {}
        self.constraints = {}

    def initialize(self, variables, domain, constraints):
        self.variables = variables
        self.domain = domain
        self.constraints = constraints
        for variable in variables:
            self.revise_queue.append((variable, domain[variable]))

    def domain_filtering(self):
        while self.revise_queue:
            revise_pair = self.revise_queue.pop(0)
            domain_reduced = self.revise(revise_pair)
            if domain_reduced:
                node = revise_pair[0]
                for edge in node.edges:
                    if len(edge.domain) != 1:
                        self.revise_queue.append((edge, edge.edges))
        return self.variables

    def revise(self, revise_pair):
        for neighbourNode in revise_pair[1]:
            if len(neighbourNode.domain) == 1:
                if (neighbourNode.domain[0] in revise_pair[0].domain):
                    revise_pair[0].domain.remove(neighbourNode.domain[0])
                    return True
        return False

    def rerun(self):
        self.revise_queue.append((node,constraints)
        self.domain_filtering()


'''
    def makefunc(var_names, expression, envir=globals()):
        args = ""
        for n in var_names:
            args = args + " ," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")", envir)
'''
