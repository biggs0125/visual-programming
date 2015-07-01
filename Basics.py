from Block import *
import Block

add = Expression("op")
add.op = lambda x, y : x + y

mult = Expression("op")
mult.op = lambda x, y : x * y

div = Expression("op")
div.op = lambda x, y : x / y

sub = Expression("op")
sub.op = lambda x, y : x - y
