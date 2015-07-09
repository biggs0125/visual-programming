from Blocks import FunctionBlock

class MapBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: 'LIST'}
    _outputType = 'LIST'
    _func = staticmethod(lambda value1, value2: [value1(value) for value in value2])

class RangeBlock(FunctionBlock):
    _inputTypes = {0: 'INT'}
    _outputType = 'LIST'
    _func = staticmethod(lambda value1: range(value1))

class FilterBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: 'LIST'}
    _outputType = 'LIST'
    _func = staticmethod(lambda value1, value2: [value for value in value2 if value1(value)])

class ReduceBlock(FunctionBlock):
    _inputTypes = {0: 'FUNC', 1: 'LIST'}
    _outputType = 'ANY'
    _func = staticmethod(lambda value1, value2: reduce(value1, value2))
