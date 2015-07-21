from Blocks import FunctionBlock
from Types import *
class MapBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = ListType(BaseType())
    _func = staticmethod(lambda value1, value2: [value1(value) for value in value2])

class RangeBlock(FunctionBlock):
    _inputTypes = {0: IntType()}
    _outputType = ListType(BaseType())
    _func = staticmethod(lambda value1: range(value1))

class FilterBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = ListType(BaseType())
    _func = staticmethod(lambda value1, value2: [value for value in value2 if value1(value)])

class ReduceBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: ListType(BaseType())}
    _outputType = BaseType()
    _func = staticmethod(lambda value1, value2: reduce(value1, value2))
