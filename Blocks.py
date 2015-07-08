from Closure import Closure

TYPES = {'INT': int, 'STR': str, 'BOOL': bool, 'LIST': list, 'SET': set, 'DICT': dict, 'ARG': 'argument', 'NONE': None}

class Block(object):
    _func = lambda: None
    _inputTypes = {}
    _outputType = None

    def __init__(self, name = None, *args, **kwargs):
        self._name = name
        self._inputs = {}
        self._inputBlocks = {}
        self._value = None

    def __str__(self):
        return "{name}: {value}".format(name=self._name if not self._name is None
                                        else self._outputType, value=self.getValue())

    def add(self, block, which = None):
        if which is None:
            which = len(self._inputBlocks)
        if not which in self._inputTypes.keys():
            raise Exception('Tried to add argument to invalid slot')
        if not self._inputTypes[which] is block.getOutputType() and not block.getOutputType() is 'ARG':
            raise Exception("Incorrect type: These blocks do not have matching types")
        if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
            raise Exception('This slot if already filled. Remove the block there first')
        self._inputBlocks[which] = block
        block._outputBlock = self

    def remove(self, which):
        if which in self._inputTypes.keys():
            if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
                self._inputBlocks[which] = None
                self.clearValue()
            else:
                raise Exception('There is no block to remove from this slot')
        else:
            raise Exception('Tried to remove argument from invalid slot')

    def clearValue(self):
        self._value = None

    def getValue(self):
        return self._value

    def missingArgs(self):
        return [k for k in self._inputTypes.keys() if not k in self._inputBlocks or self._inputBlocks[k] is None]

    def getType(self):
        types = []
        for k in self._inputTypes:
            types.add(self._inputTypes[k])
        return types

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getOutputType(self):
        return self._outputType

    def getFunction(self):
        return self._func
        
    def foldFunc(self):
        self._func.fold()

    def unfoldFunc(self):
        self._func.unfold()

    def evaluate(self):
        if len(self.missingArgs()) != 0:
            raise Exception("Not enough arguments provided")
        # Don't repeat work if we already have a value
        if self._value is not None:
            return self._value, self._outputType
        for k in self._inputBlocks:
            val = self._inputBlocks[k]
            v, t = val.evaluate()
            if t != self._inputTypes[k]:
                raise Exception("Argument type mismatch")
            self._inputs[k] = v
        self._value = self._func(*(self._inputs.values()))
        return self._value, self._outputType

    def collapseNoMissingArgs(self):
        val, valType = self.evaluate()
        block = InputBlock()
        block._type = valType
        block.add(val)
        return block

    def collapseWithMissingArgs(self, missingArgs, parentsCollapsed):
        parentsMissingArgs = {k: parent.missingArgs() for k, parent in parentsCollapsed.items()}
        block = FunctionBlock()
        block._outputType = self.getOutputType()
        parentsInfo = {k: {'func': parent.getFunction(), 'inputs': parent._inputTypes} for k, parent in parentsCollapsed.items()}
        # Get a mapping from function to parent inputs
        flattenedTypes = []
        for parentInfo in parentsInfo.values():
            flattenedTypes += [inputType for inputType in parentInfo['inputs'].values()]
        ind = 0
        remap = {}
        for k,v in parentsInfo.items():
            klen = len(v['inputs'])
            remap[k] = xrange(ind, klen + ind)
            ind += klen
        # if parents aren't missing args, flattenedTypes is []
        missingArgsMapped = [self._inputTypes[k] for k in missingArgs]
        newInputTypes = flattenedTypes + missingArgsMapped
        block._inputTypes = {i : newInputTypes[i] for i in xrange(len(newInputTypes))}
        # Join the functions for parents needing args + our function if we need an arg.
        block._func = Closure(lambda *args: self._func(*([parentsInfo[k]['func'](*[args[i] for i in l]) for k, l in remap.items()]+list(args[len(flattenedTypes):]))))
        return block

    def collapse(self):
        parentsCollapsed = {k: v.collapse() for k,v in self._inputBlocks.items() if not v is None}
        parentsMissingArgs = {k: parent.missingArgs() for k, parent in parentsCollapsed.items()}
        missingArgs = self.missingArgs()
        if all([len(args) == 0 for args in parentsMissingArgs.values()]):
            if len(missingArgs) == 0:
                return self.collapseNoMissingArgs()
        return self.collapseWithMissingArgs(missingArgs, parentsCollapsed)

class InputBlock(Block):
    _type = 'ARG'
    _func = lambda self: self._value

    def __init__(self, *args, **kwargs):
        self._outputType = 'ARG'
        if 'argType' in kwargs.keys():
            self._type = kwargs['argType']
        super(InputBlock, self).__init__(*args, **kwargs)

    def add(self, value):
        if not type(value) is TYPES[self._type]:
            raise Exception("Incorrect type: {value} does not have type {typeKey}"
                            .format(value=value, typeKey=self._type))
        self._value = value
        self._outputType = self._type

class IntBlock(InputBlock):
    _type = 'INT'

class StringBlock(InputBlock):
    _type = 'STR'

class BoolBlock(InputBlock):
    _type = 'BOOL'

class ListBlock(InputBlock):
    _type = 'LIST'

class FunctionBlock(Block):

    def __init__(self, *args, **kwargs):
        if 'outputType' in kwargs.keys():
            self.outputType = kwargs['outputType']
        super(FunctionBlock, self).__init__(*args, **kwargs)
        self._func = Closure(self._func)
        self._inputs = {i: None for i in xrange(len(self._inputTypes))} # This is the input block

class StringTransformBlock(FunctionBlock):
    _inputTypes = {0: 'STR'}
    _outputType = 'STR'

class LowerCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.lower())

class UpperCaseBlock(StringTransformBlock):
    _func = staticmethod(lambda value: value.upper())


class UnaryMathBlock(FunctionBlock):
    _inputTypes = {0: 'INT'}
    _outputType = 'INT'

class IncrementBlock(UnaryMathBlock):
    _func = staticmethod(lambda value: value + 1)

class BinaryMathBlock(FunctionBlock):
    _inputTypes = {0: 'INT', 1: 'INT'}
    _outputType = 'INT'
    _func = staticmethod(lambda value1, value2: None)

class PlusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 + value2)

class MinusBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 - value2)

class MultBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 * value2)

class DivBlock(BinaryMathBlock):
    _func = staticmethod(lambda value1, value2: value1 / value2)

class MapBlock(FunctionBlock):
    _inputTypes = {0: 'ARG', 1: 'LIST'}
