from Blocks import FunctionBlock

class EqualsBlock(FunctionBlock):
    _inputTypes = {0: 'ANY', 1: 'ANY'}
    _outputType = 'BOOL'
    _func = staticmethod(lambda value1, value2: value1 == value2)
