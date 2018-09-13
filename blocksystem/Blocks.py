from Types import TypeVar

class Block(object):
    def __init__(self, type, *args):
        self._type = type
        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = self.__class__.__name__
        self._func = lambda: None
        self._value = None
        self._collapsedCopy = None

    def __str__(self):
        return "{name}: {value}".format(name=self._name if not self._name is None
                                        else self._type, value=self.getValue())
    
    def clearCache(self):
        self._collapsedCopy = None

    def collapse(self):
        return self

    def getOutputType(self):
        return self._type
        
    def getType(self):
        return self._type

class FunctionBlock(Block):
    def __init__(self, type, *args):
        self._arity = len(type.getInputTypes())
        self._args = [None] * self._arity
        super(FunctionBlock, self).__init__(type, *args) 

    def addArg(self, arg, argNumber):
        if argNumber >= arity or argNumber < 0:
            raise Exception('Cannot add arg to out of bounds slot.')

        inputType = self.getType().getInputTypes()[argNumber]
        argOutputType = arg.getOutputType()

        # Make sure the type of the arg matches the expected arg type
        if not inputType == argOutputType:
            return False

        self._args[argNumber] = arg

        # Check to see if the arg slot is a typevar and substitute if it is
        if inputType.KEY == TypeVar.KEY and not inputType.isSubstituted():
            self.getType().substitute(inputType, argOutputType)
        # Check to see if the arg outputs a typevar and substitute for it if it is
        if argOutputType.KEY == TypeVar.KEY and not argOutputType.isSubstituted():
            arg.getType().substitute(argOutputType, argInputType)
        return True
    
    def removeArg(self, argNumber):
        if argNumber >= arity or argNumber < 0:
            raise Exception('Cannot add arg to out of bounds slot.')
        # Check to see if the arg is a typevar and substitute if it is
        if inputType.KEY == TypeVar.KEY and inputType.isSubstituted():
            self.getType().unsubstitute(inputType)
    
    def getOutputType(self):
        return self._type.getOutputType()
        
        
        
