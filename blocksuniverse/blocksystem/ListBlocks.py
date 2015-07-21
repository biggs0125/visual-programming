from Blocks import FunctionBlock
from Types import *
class MapBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = ListType(BaseType())
    _func = staticmethod(lambda value1, value2: [value1(value) for value in value2])
    def __init__(self, argType = BaseType(), resType = BaseType()):
        _inputTypes[0] = FunctionType([argType], resType)
        _inputTypes[1] = ListType(argType)

class RangeBlock(FunctionBlock):
    _inputTypes = {0: IntType()}
    _outputType = ListType(IntType())
    _func = staticmethod(lambda value1: range(value1))

class FilterBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = ListType(BaseType())
    _func = staticmethod(lambda value1, value2: [value for value in value2 if value1(value)])
    def __init__(self, argType = BaseType()):
        _inputTypes[0] = FunctionType([argType], BoolType())
        _inputTypes[1] = ListType(argType)
        _outputType = ListType(argType)
class ReduceBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = BaseType()
    _func = staticmethod(lambda value1, value2: reduce(value1, value2))
    def __init__(self, argType = BaseType()):
        _inputTypes[0] = FunctionType([argType, argType], argType)
        _inputTypes[1] = ListType(argType)
        _outputType = argType
