import Test
import cPickle
from Closure import Closure
from Blocks import Block

block1 = Test.e1
print block1.evaluate()
c = Closure(block1._func)
block1._func = c
block1str = cPickle.dumps(block1)
block2 = cPickle.loads(block1str)
print block2.evaluate()
