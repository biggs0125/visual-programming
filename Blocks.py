TYPES = {'INT': int, 'STR': str, 'BOOL': bool, 'NONE': None}

def typeCheck(value, typeKey):
    if type(value) is TYPES[typeKey] or value is TYPES[typeKey]:
        return True
    raise Exception("Incorrect type: " + 
                    str(value) +
                    " does not have type " + 
                    typeKey)

class Block:
    def evaluate(self):
        return None

class InputBlock(Block):
    _type = None
    _value = None

    def add(self, newVal):
        if typeCheck(newVal, self._type):
            self._value = newVal
        else:
            raise Exception

    def evaluate(self):
        return self._value

class IntInputBlock(InputBlock):
    _type = 'INT'

class StringInputBlock(InputBlock):
    _type = 'STR'

class BoolInputBlock(InputBlock):
    _type = 'BOOL'

class OperatorBlock(Block):
    _inputTypes = {}
    _outputType = None
    
    def __init__(self):
        self._inputs = {i: None for i in xrange(len(self._inputTypes))} # This is the input block
        self._outputValue = None # This is the output value

    def add(self, block, which):
        if which in self._inputTypes.keys():
            self._inputs[which] = block
        else:
            raise Exception('Invalid argument slot')

    def evaluate(self):
        if None in self._inputs.values():
            raise Exception("Not enough arguments provided")
        func_inputs = {k: v.evaluate() for k,v in self._inputs.items()}
        if all([typeCheck(v, self._inputTypes[k]) for k,v in func_inputs.items()]):
            self._outputValue = self._func(*func_inputs.values())
            if typeCheck(self._outputValue, self._outputType):
                return self._outputValue
            else:
                self._outputValue = None

    
class IncrementBlock(OperatorBlock):
    _inputTypes = {0: 'INT'}
    _outputType = 'INT'
    _func = staticmethod(lambda value: value + 1)

class LowerCaseBlock(OperatorBlock):
    _inputTypes = {0: 'STR'}
    _outputType = 'STR'
    _func = staticmethod(lambda value: value.lower())

class BinaryMathBlock(OperatorBlock):
    _inputTypes = {0: 'INT', 1: 'INT'}
    _outputType = 'INT'
    _func = staticmethod(lambda value1, value2: None)

class PlusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 + value2)

class MinusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 - value2)

class MultBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 * value2)

class DivBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 / value2)
    

# Add 7 to input block
v = IntInputBlock()
v.add(7)
print v.evaluate()

# Add string 'HI' to input block
x = StringInputBlock()
x.add("HI")
print x.evaluate()

# Increment 7 in v
i = IncrementBlock()
i.add(v, 0)
print i.evaluate()

# Make 'HI' in x all lower
j = LowerCaseBlock()
j.add(x, 0)
print j.evaluate()

# Add v and i
p = PlusBlock()
p.add(v, 0)
p.add(i, 1)
print p.evaluate()

# Increment z
z = IncrementBlock()
z.add(p, 0)
print z.evaluate()
