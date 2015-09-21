class GAC():
	'''
	The General Arc-Consistency Algorithm
    '''


    def __init__():

    def solve():
        initialize()
        if not solution:(tomt domene på en node)
            astar search


    def initialize():

        #need to fill up queue with focalvariable-constraint pairs
        revise_queue = []
        domain_filtering(revise_queue)

    def domain_filtering(revise_queue):
    	while revise_queue:
    		revise_pair = self.revise_queue.pop(0)
    		domain_reduced = revise(revise_pair)
    		if domain_reduced:
    			revise_queue.push(alle naboer)



    def rerun():
    	for all constraints where X appears:
    		self.revise_queue.push(pairs)
    	domain_filtering()

   	def revise(focal_variable, constraint):
    	return None

    def makefunc(var_names, expression, envir=globals()):
    	args = ""
    	for n in var_names:
    		args = args + " ," + n
    	return eval("(lambda " + args[1:] + ": " + expression + ")", envir)
