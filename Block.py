class Scope:
    def __init__(self, oldscope = None):
        self.prev = oldscope
        self.dict = {}
    def __getitem__(self, index):
        cur = self
        while cur is not None:
            if index in cur.dict:
                return cur.dict[index]
            cur = cur.prev
    def __setitem__(self, key, value):
        self.dict[key] = value
    def __delitem__(self, index):
        cur = self
        while cur is not None:
            if index in cur.dict:
                del cur.dict[index]
                return
            cur = cur.prev
class Expression:
    def __init__(self, name):
        self.name = name
class Function:
    def __init__(self, expressions, argTypes, argNames):
        self.expressions = expressions
        self.argTypes = argTypes
        self.argNames = argNames
class Metadata:
    def __init__(self):
        self.isDone = False
# Evaluates a set of expressions, stopping at a return statement and
# returning that value. Works if return statement is omitted
def evaluateMultipleExpressions(metadata, scope, exprs):
    val = None
    for expr in exprs:
        val = evaluate(metadata, scope, expr)
        if (metadata.isDone):
            return val
    return val

def evaluateFunctionCall(metadata, scope, funcName, args):
    # Find function
    function = scope[funcName]
    # Add arguments to scope
    newscope = Scope(scope)
    for i in xrange(len(args)):
        newscope[function.argNames[i]] = args[i]
    return evaluateMultipleExpressions(metadata, newscope, function.expressions)
def evaluate(metadata, scope, expr):
    if expr.name == "value":
        return expr.value # A value is terminal
    elif expr.name == "var":
        return scope[expr.varName]
    elif expr.name == "assignment": # Assignments only change scope
        n = expr.varName
        e = evaluate(metadata, scope, expr.expression)
        scope[n] = e
        return None
    elif expr.name == "functionCall":
        return evaluateFunctionCall(metadata, scope, expr.func, expr.args)
    elif expr.name == "return":
        metadata.isDone = True
        return evaluate(expr.expression)
    elif expr.name == "if":
        if evaluate(expr.condition):
            return evaluateMultipleExpressions(metadata, scope, expr.ifExpressions)
        else:
            return evaluateMultipleExpressions(metadata, scope, expr.elseExpressions)
    elif expr.name == "functionDef":
        func = Function(expr.expressions, expr.argTypes, expr.argNames)
        name = expr.funcName
        scope[name] = func
        return None
    # Operators that act on 2 elements (+, /, *, etc)
    elif expr.name == "op":
        return expr.op(evaluate(metadata, scope, expr.left),
                       evaluate(metadata, scope, expr.right))
