from Blocks import FunctionBlock

class UnaryLogicBlock(FunctionBlock):
    _inputTypes = {0: 'BOOL'}
    _outputType = 'BOOL'

class NotBlock(UnaryLogicBlock):
    _func = staticmethod(lambda value1: not value1)

class BinaryLogicBlock(FunctionBlock):
    _inputTypes = {0: 'BOOL', 1: 'BOOL'}
    _outputType = 'BOOL'

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
    _inputTypes = {0: 'BOOL', 1: 'ANY', 2: 'ANY'}
    _outputType = 'ANY'
    _func = staticmethod(lambda value1, value2, value3: value2 if value1 else value3)
