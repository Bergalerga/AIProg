class Constraints():
	'''
	Expression is how the constraint is defined, ex x != y
	Involved is a list of all variables involved in constraint, in this case all rows are involved for a column, and all columns are involved for a row
	'''
	def __init__(self, expression, involved):
		self.expression = expression
		self.involved = involved

	def contains(self, variable):
        if variable in self.involved:
            return True
        return False
		
	def makefunc (self, var_names , expression , envir = globals()):
		args = ",".join(var_names)
		return eval("(lambda " + args + ": " + expression + ")" , envir)