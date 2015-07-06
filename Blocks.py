from types import *

TYPES = {'INT': int, 'STR': str, 'BOOL': bool, 'LIST': list, 'SET': set, 'DICT': dict, 'ARG': 'argument', 'NONE': None}

class Block(object):
    _func = lambda: None
    _inputTypes = {}
    _outputType = None

    def __init__(self, name = None, *args, **kwargs):
        self._name = name
        self._inputs = {}
        self._inputBlocks = {}
        self._value = None

    def __str__(self):
        return "{name}: {value}".format(name=self._name if not self._name is None
                                        else self._outputType, value=self.getValue())

    def add(self, block, which = None):
        if which is None:
            which = len(self._inputBlocks)
        if not which in self._inputTypes.keys():
            raise Exception('Tried to add argument to invalid slot')
        if not self._inputTypes[which] is block.getOutputType() and not block.getOutputType() is 'ARG':
            raise Exception("Incorrect type: These blocks do not have matching types")
        if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
            raise Exception('This slot if already filled. Remove the block there first')
        self._inputBlocks[which] = block
        block._outputBlock = self

    def remove(self, which):
        if which in self._inputTypes.keys():
            if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
                self._inputBlocks[which] = None
                self.clearValue()
            else:
                raise Exception('There is no block to remove from this slot')
        else:
            raise Exception('Tried to remove argument from invalid slot')

    def clearValue(self):
        self._value = None

    def getValue(self):
        return self._value

    def getType(self):
        types = []
        for k in self._inputTypes:
            types.add(self._inputTypes[k])
        return types

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getOutputType(self):
        return self._outputType

    def evaluate(self):
        # Don't repeat work if we already have a value
        if self._value is not None:
            return self._value, self._outputType
        if len(self._inputBlocks) != len(self._inputTypes):
            raise Exception("Not enough arguments provided")
        for k in self._inputBlocks:
            val = self._inputBlocks[k]
            v, t = val.evaluate()
            if t != self._inputTypes[k]:
                raise Exception("Argument type mismatch")
            self._inputs[k] = v
        self._value = self._func(*(self._inputs.values()))
        return self._value, self._outputType

class InputBlock(Block):
    _type = 'ARG'
    _func = lambda self: self._value

    def __init__(self, *args, **kwargs):
        self._outputType = 'ARG'
        if 'argType' in kwargs.keys():
            self._type = kwargs['argType']
        super(InputBlock, self).__init__(*args, **kwargs)

    def add(self, value):
        if not type(value) is TYPES[self._type]:
            raise Exception("Incorrect type: {value} does not have type {typeKey}"
                            .format(value=value, typeKey=self._type))
        self._value = value
        self._outputType = self._type

class IntBlock(InputBlock):
    _type = 'INT'

class StringBlock(InputBlock):
    _type = 'STR'

class BoolBlock(InputBlock):
    _type = 'BOOL'

class ListBlock(InputBlock):
    _type = 'LIST'

class FunctionBlock(Block):

    def __init__(self, *args, **kwargs):
        if 'outputType' in kwargs.keys():
            self.outputType = kwargs['outputType']
        super(FunctionBlock, self).__init__(*args, **kwargs)
        self._inputs = {i: None for i in xrange(len(self._inputTypes))} # This is the input block

class StringTransformBlock(FunctionBlock):
    _inputTypes = {0: 'STR'}
    _outputType = 'STR'

class LowerCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.lower())

class UpperCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.upper())


class UnaryMathBlock(FunctionBlock):
    _inputTypes = {0: 'INT'}
    _outputType = 'INT'

class IncrementBlock(UnaryMathBlock):
    _func = staticmethod(lambda value: value + 1)

class BinaryMathBlock(FunctionBlock):
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

class MapBlock(FunctionBlock):
    _inputTypes = {0: 'ARG', 1: 'LIST'}
