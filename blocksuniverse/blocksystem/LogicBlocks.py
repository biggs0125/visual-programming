from Blocks import FunctionBlock
from Types import *
class UnaryLogicBlock(FunctionBlock):
    _inputTypes = {0: BoolType()}
    _outputType = BoolType()

class NotBlock(UnaryLogicBlock):
    _func = staticmethod(lambda value1: not value1)

class BinaryLogicBlock(FunctionBlock):
    _inputTypes = {0: BoolType(), 1: BoolType()}
    _outputType = BoolType()

class AndBlock(BinaryLogicBlock):
    _func = staticmethod(lambda value1, value2: value1 and value2)

class OrBlock(BinaryLogicBlock):
    _func = staticmethod(lambda value1, value2: value1 or value2)

class XorBlock(BinaryLogicBlock):
    _func = staticmethod(lambda value1, value2: value1 != value2)

class NorBlock(BinaryLogicBlock):
    _func = staticmethod(lambda value1, value2: not(value1 or value2))

class NandBlock(BinaryLogicBlock):
    _func = staticmethod(lambda value1, value2: not(value1 and value2))

class TernaryBlock(FunctionBlock):
    _inputTypes = {0:  BoolType(), 1: BaseType(), 2: BaseType()}
    _outputType = BaseType()
    _func = staticmethod(lambda value1, value2, value3: value2 if value1 else value3)
