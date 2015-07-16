class BaseType:
    def __init__(self):
        self.type = 'ANY'
        self.paramTypes = []
    # The type-matching function. Note that a matches b does not imply
    # b matches a, because ANY can bind to anything, but INT doesn't accept
    # any.
    def matches(self, otherType):
        if self.type == 'ANY':
            return True
        didMatch = self.type == otherType.type
        if len(self.paramTypes) != otherType.paramTypes:
            return False
        for i in xrange(len(self.paramTypes)):
            didMatch = didMatch and self.paramTypes[i].\
                       matches(otherType.paramTypes[i])
        return self.type == otherType.type

class IntType(BaseType):
    def __init__(self):
        self.type = 'INT'
        self.paramTypes = []
class StrType(BaseType):
    def __init__(self):
        self.type = 'STR'
        self.paramTypes = []
class BoolType(BaseType):
    def __init__(self):
        self.type = 'BOOL'
        self.paramTypes = []
class ListType(BaseType):
    def __init__(self, elementType):
        self.type = 'LIST'
        self.paramTypes = [elementType]

class SetType(BaseType):
    def __init__(self, elementType):
        self.type = 'SET'
        self.paramTypes = [elementType]

class DictType(BaseType):
    def __init__(self, keyType, valType):
        self.type = 'DICT'
        self.paramTypes = [keyType, valType]
