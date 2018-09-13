from InputBlocks import *
from MathBlocks import *
from LogicBlocks import *
from MiscBlocks import *
from ListBlocks import *
from Types import *
import cPickle
from Closure import Closure
from Blocks import Block

class Tests(object):
    @staticmethod
    def runTests():
        return

class AllTests(Tests):
    @staticmethod
    def runTests():
        TypeTests.runTests()
        CollapseTests.runTests()
        LogicTests.runTests()
        ListTests.runTests()
        SerializeTests.runTests()

class TypeTests(Tests):
    @staticmethod
    def runTests():
        print "\n################# TYPE TESTS ###################\n"
        print "\n############# Print Types ###############\n"
        print StringType()
        print IntType()
        print BoolType()
        print ListType(BoolType())
        print TupleType(IntType(), StringType(), BoolType())
        print TupleType(IntType(), StringType(), FunctionType(IntType(), BoolType()))
        print FunctionType(IntType(), BoolType())
        print DictType(StringType(), IntType())
        print TypeVar()
        print TypeVar()
        print "\n############# Substitute Types ###############\n"
        tyvar = TypeVar()
        alphaList = ListType(tyvar)
        print alphaList
        alphaList.substitute(tyvar, StringType())
        print alphaList
        alphaList.unsubstitute(TypeVar())
        print alphaList
        alphaList.unsubstitute(tyvar)
        print alphaList
        print "\n############# Running compare type tests with asserts ###############\n"
        assert not DictType(BoolType(), IntType()) == DictType(BoolType(), StringType())
        assert DictType(BoolType(), IntType()) == DictType(BoolType(), IntType())
        assert DictType(BoolType(), IntType()) == DictType(TypeVar(), IntType())
        assert DictType(BoolType(), IntType()) == DictType(TypeVar(), TypeVar())
        assert DictType(BoolType(), TypeVar()) == DictType(TypeVar(), TypeVar())
        alphaStringDict = DictType(tyvar, StringType())
        assert alphaStringDict == DictType(BoolType(), StringType())
        alphaStringDict.substitute(tyvar, IntType())
        assert not alphaStringDict == DictType(BoolType(), StringType())
        assert alphaStringDict == DictType(IntType(), StringType())
        assert alphaStringDict == DictType(TypeVar(), StringType())
        alphaStringDict.unsubstitute(tyvar)
        assert alphaStringDict == DictType(BoolType(), StringType())
        assert alphaStringDict == DictType(IntType(), StringType())
        assert alphaStringDict == DictType(TypeVar(), StringType())
        
        

class CollapseTests(Tests):
    @staticmethod
    def runTests():
        print "\n################# COLLAPSE TESTS ###################\n"
        # Collapse fully evaluable
        print "Testing collapse with no missing args, expect (10, INT)"
        x = PlusBlock()
        a = IntBlock()
        b = IntBlock()
        y = PlusBlock()
        a.add(3)
        b.add(4)
        x.add(a)
        x.add(b)
        y.add(a)
        y.add(x)
        n = y.collapse()
        print n.evaluate()
        
        # Collapse with only block missing args
        print "Testing collapse with only current block missing args, expect (132, INT)"
        g = PlusBlock()
        h = PlusBlock()
        w = IntBlock()
        k = IntBlock()
        w.add(9)
        k.add(23)
        g.add(h)
        h.add(w)
        h.add(k)
        u = g.collapse()
        c = IntBlock()
        c.add(100)
        u.add(c)
        print u.evaluate()

        # Collapse with only parents missing args
        print "Testing collapse with only parents missing args, expect (26, INT)"
        q2 = PlusBlock()
        t2 = PlusBlock()
        f2 = PlusBlock()
        f2.add(q2)
        f2.add(t2)
        e2 = f2.collapse()
        j1 = IntBlock()
        j1.add(5)
        j2 = IntBlock()
        j2.add(6)
        j3 = IntBlock()
        j3.add(7)
        j4 = IntBlock()
        j4.add(8)
        e2.add(j1)
        e2.add(j2)
        e2.add(j3)
        e2.add(j4)
        print e2.evaluate()


        # Collapse with both parents and block missing args
        print "Testing collapse where both parent and block are missing args, expect (18, INT)"
        q1 = PlusBlock()
        f1 = PlusBlock()
        f1.add(q1)
        e1 = f1.collapse()
        i1 = IntBlock()
        i1.add(5)
        i2 = IntBlock()
        i2.add(6)
        i3 = IntBlock()
        i3.add(7)
        e1.add(i1)
        e1.add(i2)
        e1.add(i3)
        print e1.evaluate()

        def ib(n):
            resBlock = IntBlock()
            resBlock.add(n)
            return resBlock
            # Three level collapse
        print "Testing 3 level collapse, expect (22, INT)"
        a1 = PlusBlock()
        b1 = PlusBlock()
        c1 = PlusBlock()
        b1.add(a1)
        c1.add(b1)
        f1 = c1.collapse()
        for i in xrange(4):
            f1.add(ib(i + 4))
        print f1.evaluate()

class LogicTests(Tests):
    @staticmethod
    def runTests():
        print "\n################# LOGIC TESTS ###################\n"
        true = BoolBlock()
        true.add(True)
        false = BoolBlock()
        false.add(False)
        print "Testing AndBlock(true, false), expect (False, BOOL)"
        a = AndBlock(true, false)
        print a.evaluate()
        print "Testing AndBlock(true, true), expect (True, BOOL)"
        b = AndBlock(true, true)
        print b.evaluate()
        print "Testing OrBlock(false, true), expect (True, BOOL)"
        c = OrBlock(false, true)
        print c.evaluate()
        print "Testing NotBlock(true), expect (False, BOOL)"
        d = NotBlock(true)
        print d.evaluate()
        print "Testing collapsed Nand(true, true) == NandBlock(true, true), expect (True, BOOL)"
        e = AndBlock()
        f = NotBlock(e)
        g = f.collapse()
        g.add(true)
        g.add(true)
        h = NandBlock(true, true)
        i = EqualsBlock(h, g)
        print i.evaluate()

class ListTests(Tests):
    @staticmethod
    def runTests():
        print "\n################# LIST TESTS ###################\n"
        print "Testing [1,3,5,7] == filter(isOdd,xrange(8)), expect (True, BOOL)"
        list1 = ListBlock([1,3,5,7])
        list2 = RangeBlock(IntBlock(8))
        mod2 = ModBlock(None, IntBlock(2))
        isOdd = EqualsBlock(mod2, IntBlock(1))
        odds = FilterBlock(isOdd, list2)
        print EqualsBlock(odds, list1).evaluate()
        print "Testing map(double, [0,1,2,3]) == [0,2,4,6] expect (True, BOOL)"
        list3 = ListBlock([0,2,4,6])
        double = MultBlock(IntBlock(2), None)
        list4 = RangeBlock(IntBlock(4))
        mapped = MapBlock(double, list4)
        print EqualsBlock(mapped, list3).evaluate()
        print "Testing reduce(plus, range(4)) == 6 expect (True, BOOL)" 
        plus = PlusBlock()
        sumblock = ReduceBlock(plus)
        list5 = RangeBlock(IntBlock(4))
        sumblock.add(list5)
        print EqualsBlock(sumblock, IntBlock(6)).evaluate()


class SerializeTests(Tests):
    @staticmethod
    def runTests():
        print "\n################# SERIALIZE TESTS ###################\n"
        x = PlusBlock()
        a = IntBlock()
        b = IntBlock()
        y = PlusBlock()
        a.add(3)
        b.add(4)
        x.add(a)
        x.add(b)
        y.add(a)
        y.add(x)
        print y.evaluate()
        y.foldFunc()
        ystr = cPickle.dumps(y)
        newy = cPickle.loads(ystr)
        print newy.evaluate()
        list1 = ListBlock([1,3,5,7])
        list2 = RangeBlock(IntBlock(8))
        mod2 = ModBlock(None, IntBlock(2))
        isOdd = EqualsBlock(mod2, IntBlock(1))
        odds1 = FilterBlock(isOdd, list2)
        print odds1.evaluate()
        odds1.foldFunc()
        odds1str = cPickle.dumps(odds1)
        odds2 = cPickle.loads(odds1str)
        print odds2.evaluate()
        print "#########################################"

AllTests.runTests()
