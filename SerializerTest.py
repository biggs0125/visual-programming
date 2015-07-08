import Test
import cPickle
from Closure import Closure
from Blocks import Block

print "###########Serialize Tests###############"
block1 = Test.e1
print block1.evaluate()
block1.foldFunc()
block1._func = Closure(block1._func)
block1._func.fold()
block1str = cPickle.dumps(block1)
block2 = cPickle.loads(block1str)
print block2.evaluate()
print "#########################################"
