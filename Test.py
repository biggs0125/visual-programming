from Blocks import *

i = IntBlock('i')
i.add(7)

print i

j = IntBlock('j')
j.add(100)

print i
print j

k = PlusBlock('k')
k.add(j, 0)
k.add(i, 1)
i.evaluate()

print i
print j
print k

l = IncrementBlock('l')
l.add(k, 0)
i.evaluate()

print i
print j
print k
print l

a = StringBlock('a')
a.add('Yo')

print a

b = UpperCaseBlock('b')
b.add(a, 0)
a.evaluate()

print a
print b

c = LowerCaseBlock('c')
c.add(b, 0)
a.evaluate()

print a
print b
print c

x = collapse(i)
x.setName('x')
print x
