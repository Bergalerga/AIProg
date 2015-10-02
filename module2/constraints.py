class Constraints():
	'''
	Expression is how the constraint is defined, ex x != y
	Involved is a dict where keys are nodes and items are who is connected to the key
	'''
	def __init__(self, expression, var_list, involved):
		self.expression = self.makefunc(var_list, expression)
		self.involved = involved

	def contains(self, variable):
		if variable in self.involved:
			return True
		return False
		
	def makefunc (self, var_names , expression , envir = globals()):
		args = ",".join(var_names)
		return eval("(lambda " + args + ": " + expression + ")" , envir)

	def satisfies(self, other):
		'''

		'''
		pass
