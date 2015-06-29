from enum import Enum

class Type(Enum):
    int = 1
    string = 2
    pair = 3
    function = 4
    void = 5

"""
     Merges two scopes dictionaries A and B, handling conflicts by
     keeping the elements of B.
"""
def merge(scopeA, scopeB):
    res = {}
    for k in scopeA:
        res[k] = scopeA[k]
    for k in scopeB:
        res[k] = scopeB[k]
    return res

# Expressions are either an assignment, function, value,
# or a list of expressions.
# An assignment is a tuple of (name, assigned value),
# a function is a map from input value to output value,
# and a value is an expression that evaluates no further.
# There is a stack of scopes being built as expressions get evaluated.
# If an expression is a simple one, such as assignment, it keeps the old
# scope stack.
# If the expression is in a new scope, it pushes a new scope to the stack.
# When looking for a value, we go up the stack, starting with the most
# recently added scope.
# Expressions are ran with a starting scope stack.
class Expression:
    def __init__(self, type = Type.int, subexpressions = []):
        """
        @param           type: the type that this expression evaluates to,
                               when used as a rvalue
        @param subexpressions: the list of expressions that this expression
                               encompasses
        """
        self.type = type
        self.subexpressions = subexpressions
    # Evaluates the expression, modifying the scope stack
    def evaluate(self, scopeStack = []):
        # For each expression, pipe the result of the previous
        # expression to the next expression.
        res = null
        for se in subexpressions:
            res = se.evaluate(scopeStack)
        return res

class Value(Expression):
    def __init__(self, type = Type.int, value = 0):
        self.type = type
        self.value = value
    def evaluate(self, scopeStack, args):
        return value

class Function():
    def __init__(self, argNames, expressions):
        self.expressions = expressions
        self.argNames = argNames
    def evaluate(self, scopeStack):
        for ex in expressions:
            ex.evaluate(scopeStack)
# Arguments must be in correct order
class FunctionCall():
    def __init__(self, function, args):
        self.function = function
        self.args = args
    def evaluate(self, scopeStack, args):
        scope = scopeStack.copy()
        # Add the argument variables to the function
        for i in xrange(args):
            scope[self.function.argNames[i]] = args[i]
        return self.function.evaluate(scope)

# todo: a class for return expressions
class Return():
    pass

# todo: an assignment operator. Basically, add result of expression to scope
class Assignment():
    pass
