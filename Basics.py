from Block import *
import Block

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
