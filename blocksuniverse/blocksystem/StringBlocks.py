from Blocks import FunctionBlock

class StringTransformBlock(FunctionBlock):
    _inputTypes = {0: StrType()}
    _outputType = StrType()

class LowerCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.lower())

class UpperCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.upper())
