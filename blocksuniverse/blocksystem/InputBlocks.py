from Blocks import InputBlock
from Types import *
class IntBlock(InputBlock):
    _type = IntType()

class StringBlock(InputBlock):
    _type = StrType()

class BoolBlock(InputBlock):
    _type = BoolType()

# Right now, list(str) = list(int).
# TODO: Change constructor so that listblock has an init function that
# sets this type.
class ListBlock(InputBlock):
    _type = ListType(BaseType())
