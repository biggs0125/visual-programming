from Blocks import *
import copy

x = PlusBlock()

a = IntBlock()
b = IntBlock()
a.add(3)
b.add(4)

x.add(a)
x.add(b)

y = PlusBlock()
y.add(a)
y.add(x)

print y.evaluate()
