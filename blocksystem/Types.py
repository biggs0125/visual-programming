class Type(object):
    _name = ""
    _arity = 0
    _formatStr = None
    _typeKey = None

    def __init__(self, *args):
        self._typeArgs = []
        numArgs = len(args)
        if numArgs != self._arity:
            raise Exception('Expected {arity} type arguments but got {actual}.'.format(arity=arity, actual=numArgs))
        for argType in args:
            self._typeArgs.append(argType)

    def __str__(self):
        if self._formatStr is None:
            return self._name
        return self._formatStr.format(*self._typeArgs)

    def __eq__(self, otherType):
        if otherType.KEY == TypeVar.KEY:
            return otherType == self
        if self.KEY != otherType.KEY:
            return False
        return all([self._typeArgs[i] == otherType._typeArgs[i] for i in range(self._arity)])

    def substitute(self, typeVar, newType):
        for typeArg in self._typeArgs:
            typeArg.substitute(typeVar, newType)

    def unsubstitute(self, typeVar):
        for typeArg in self._typeArgs:
            typeArg.unsubstitute(typeVar)

class TypeVar(Type):
    _arity = 0
    _name = "TyVar"
    _id = 0
    KEY = "TYVAR"

    def __init__(self):
        self.__class__._id += 1
        self._id = self.__class__._id
        self._subbedType = None

    def __eq__(self, otherType):
        if self._subbedType is None:
            return True
        return self._subbedType == otherType

    def substitute(self, typeVar, newType):
        if typeVar._id == self._id:
            self._subbedType = newType
            self._formatStr = newType._formatStr

    def unsubstitute(self, typeVar):
        if typeVar._id == self._id:
            self._subbedType = None
            self._formatStr = None

    def isSubstituted(self):
        return not self._subbedType is None

    def __str__(self):
        if self._subbedType:
            return str(self._subbedType)
        return "TYVAR_{id}".format(id=self._id)


class IntType(Type):
    _arity = 0
    _name = "int"
    KEY = 'INT'

class StringType(Type):
    _arity = 0
    _name = "string"
    KEY = "STRING"

class BoolType(Type):
    _arity = 0
    _name = "bool"
    KEY = "BOOL"

class TupleType(Type):
    KEY = "TUP"

    def __init__(self, *args):
        self._arity = len(args)
        self._formatStr = "(" + ", ".join(["{" + str(i) + "}" for i in range(self._arity)]) + ")"
        super(TupleType, self).__init__(*args)

class FunctionType(Type):
    _name = "Function"
    _formatStr = "{0} -> {1}"
    KEY = "FUNC"

    def __init__(self, *args):
        if len(args) < 2:
            raise Exception('Functions must have at least 2 argument types')
        self._arity = len(args)
        inputsStr = ["{" + str(i) + "}" for i in range(self._arity-1)]
        self._formatStr = "(" + ", ".join(inputsStr) + ") -> {" + str(self._arity-1) + "}"
        super(FunctionType, self).__init__(*args)
        
    def getOutputType(self):
        return self._typeArgs[-1]
    
    def getInputTypes(self):
        return self._typeArgs[:-1]

class ListType(Type):
    _arity = 1
    _name = "List"
    _formatStr = "{0} list"
    _TypeKey = "LIST"

class DictType(Type):
    _arity = 2
    _name = "Dict"
    _formatStr = "{0},{1} dict"
    KEY = "DICT"
