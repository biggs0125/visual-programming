from Blocks import FunctionBlock
from Types import *
class EqualsBlock(FunctionBlock):
    _inputTypes = {0: BaseType(), 1: BaseType()}
    _outputType = BoolType()
    _func = staticmethod(lambda value1, value2: value1 == value2)

class NotBlock(FunctionBlock):
    _inputTypes = {0: BoolType()}
    _outputType = BoolType()
    _func = staticmethod(lambda value1: not value1)
