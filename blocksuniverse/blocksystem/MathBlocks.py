from Blocks import FunctionBlock
from Types import *
class UnaryMathBlock(FunctionBlock):
    _inputTypes = {0: IntType()}
    _outputType = IntType()

class IncrementBlock(UnaryMathBlock):
    _func = staticmethod(lambda value: value + 1)

class DecrementBlock(UnaryMathBlock):
    _func = staticmethod(lambda value: value - 1)

class BinaryMathBlock(FunctionBlock):
    _inputTypes = {0: IntType(), 1: IntType()}
    _outputType = IntType()
    _func = staticmethod(lambda value1, value2: None)

class PlusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 + value2)

class MinusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 - value2)

class MultBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 * value2)

class DivBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 / value2)

class ModBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 % value2)
