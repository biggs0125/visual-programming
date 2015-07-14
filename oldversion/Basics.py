from Block import *
import Block
def val(literal):
    res = Expression("value")
    res.value = literal
    return res
a = Expression("var")
a.varName = "a"
b = Expression("var")
b.varName = "b"

add = Expression("op")
add.op = lambda x, y : x + y
add.left = a
add.right = b
mult = Expression("op")
mult.op = lambda x, y : x * y
mult.left = a
mult.right = b
div = Expression("op")
div.op = lambda x, y : x / y
div.left = a
div.right = b
sub = Expression("op")
sub.op = lambda x, y : x - y
sub.left = a
sub.right = b
class Type:
    int = 1
addFunction = Function([add], [Type.int, Type.int], ["a", "b"])

scope = Scope()
scope["add"] = addFunction
fnCall = Expression("functionCall")
fnCall.func = "add"
fnCall.args = [1, 2]
metadata = Metadata()
print evaluate(metadata, scope, fnCall)

v1 = val(13)
v2 = val(17)
gt = Expression("op")
gt.op = lambda x, y: x > y
gt.left = v1
gt.right = v2
ifCond = Expression("if")
ifCond.condition = gt
ifCond.ifExpressions = [fnCall]
ifCond.elseExpressions = []

print evaluate(metadata, scope, ifCond)
