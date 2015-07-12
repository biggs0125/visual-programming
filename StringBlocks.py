from Blocks import FunctionBlock

class StringTransformBlock(FunctionBlock):
    _inputTypes = {0: 'STR'}
    _outputType = 'STR'

class LowerCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.lower())

class UpperCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.upper())

class SplitBlock(FunctionBlock):
    _inputTypes = {0: 'STR', 1: 'STR'}
    _outputType = 'LIST'
    _func = staticmethod(lambda value1, value2: value1.split(value2))

class ReplaceBlock(FunctionBlock):
    _inputTypes = {0: 'STR', 1: 'STR', 2: 'STR'}
    _outputType = 'STR'
    _func = staticmethod(lambda value1, value2, value3: value1.replace(value2, value3))

class StringToIntBlock(FunctionBlock):
    _inputTypes = {0: 'STR'}
    _outputType = 'INT'
    _func = staticmethod(lambda value: int(value))

class StringToFloatBlock(FunctionBlock):
    _inputTypes = {0: 'STR'}
    _outputTypes = 'FLOAT'
    _fund = staticmethod(lambda value: float(value))
