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

n = y.collapse()

print n.evaluate()

q = PlusBlock()
q.add(n)

m = q.collapse()

k = IntBlock()
k.add(10)
m.add(k)

print m.evaluate()
# p = q.collapse()

# f = IntBlock()
# f.add(10)

# p.add(f)

# print p.evaluate()
