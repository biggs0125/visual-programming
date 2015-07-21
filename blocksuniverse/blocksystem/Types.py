class BaseType:
    def __init__(self):
        self.type = 'ANY'
        self.paramTypes = []
        # Type constructor
        self.tycon = None
    # The type-matching function. Note that a matches b does not imply
    # b matches a, because ANY can bind to anything, but INT doesn't accept
    # any.
    def matches(self, otherType):
        if self.type == 'ANY':
            return True
        didMatch = self.type == otherType.type
        if len(self.paramTypes) != len(otherType.paramTypes):
            return False
        for i in xrange(len(self.paramTypes)):
            didMatch = didMatch and (self.paramTypes[i]).\
                       matches(otherType.paramTypes[i])
        return didMatch and self.type == otherType.type
class IntType(BaseType):
    def __init__(self):
        self.type = 'INT'
        self.paramTypes = []
        self.tycon = int
class StrType(BaseType):
    def __init__(self):
        self.type = 'STR'
        self.paramTypes = []
        self.tycon = str
class BoolType(BaseType):
    def __init__(self):
        self.type = 'BOOL'
        self.paramTypes = []
        self.tycon = bool
class ListType(BaseType):
    def __init__(self, elementType):
        self.type = 'LIST'
        self.paramTypes = [elementType]
        self.tycon = list
class SetType(BaseType):
    def __init__(self, elementType):
        self.type = 'SET'
        self.paramTypes = [elementType]
        self.tycon = set
class DictType(BaseType):
    def __init__(self, keyType, valType):
        self.type = 'DICT'
        self.paramTypes = [keyType, valType]
        self.tycon = dict
class FunctionType(BaseType):
    def __init__(self, argTypes, resType):
        self.type = 'FUNC'
        self.paramTypes = argTypes + [resType]

def getTypeFromStr(argType):
    typedict = {
        "INT": IntType(),
        "STR": StrType(),
        "BOOL": BoolType(),
        "LIST": ListType(BaseType()),
        "SET": SetType(BaseType()),
        "DICT": DictType(BaseType(), BaseType()),
        "FUNC": FunctionType(BaseType(), BaseType()),
    }
    return typedict[argType]
