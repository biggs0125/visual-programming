import Test
import cPickle
from Closure import Closure
from Blocks import Block

print "###########Serialize Tests###############"
block1 = Test.e1
print block1.evaluate()
block1.foldFunc()
block1str = cPickle.dumps(block1)
block2 = cPickle.loads(block1str)
print block2.evaluate()
block3 = Test.f1
print block3.evaluate()
block3.foldFunc()
block3str = cPickle.dumps(block3)
block4 = cPickle.loads(block3str)
print block4.evaluate()
print "#########################################"
