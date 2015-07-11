from Closure import Closure

TYPES = {'INT': int, 'STR': str, 'BOOL': bool, 'LIST': list, 'SET': set, 'DICT': dict, 'ARG': 'argument', 'NONE': None, 'ANY': 'any'}

class Block(object):
    _func = lambda: None
    _inputTypes = {}
    _outputType = None

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = self.__class__.__name__
        self._inputBlocks = {}
        self._value = None
        self._collapsedCopy = None
        self._collapsedCopyArgs = None
        for i in args:
            self.add(i)

    def __str__(self):
        return "{name}: {value}".format(name=self._name if not self._name is None
                                        else self._outputType, value=self.getValue())

    def add(self, block, which = None):
        if which is None:
            which = len(self._inputBlocks)
        if block is None:
            self._inputBlocks[which] = None
            return
        if not which in self._inputTypes.keys():
            raise Exception('Tried to add argument to invalid slot')
        if not self._inputTypes[which] == block.getOutputType() and not (block.getOutputType() == 'ARG' \
        or self._inputTypes[which] == 'ANY' or block.getOutputType() == 'ANY' or self._inputTypes[which] == 'FUNC'):
            raise Exception("Incorrect type: Expected block with return type {expected} but got block with return type {actual}".format(expected=self._inputTypes[which], 
                                                                                                                                        actual=block.getOutputType()))
        if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
            raise Exception('This slot if already filled. Remove the block there first')
        self._inputBlocks[which] = block
        block._outputBlock = self
        self.clearCache()

    def remove(self, which):
        if which in self._inputTypes.keys():
            if which in self._inputBlocks.keys() and not self._inputBlocks[which] is None:
                self._inputBlocks[which] = None
                self.clearCache()
            else:
                raise Exception('There is no block to remove from this slot')
        else:
            raise Exception('Tried to remove argument from invalid slot')

    def clearCache(self):
        self._value = None
        self._collapsedCopy = None
        self._collapsedCopyArgs = None

    def getValue(self):
        return self._value

    def missingArgs(self):
        return [k for k in self._inputTypes.keys() if not k in self._inputBlocks or self._inputBlocks[k] is None]

    def chunkMissingArgs(self):
        return self.missingArgs() or any([i.chunkMissingArgs() for i in self._inputBlocks.values() if not i is None]) 

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
        for block in self._inputBlocks.values():
            if not block is None:
                block.foldFunc()
                
    def unfoldFunc(self):
        self._func.unfold()

    def evaluate(self, collapse=False):
        if collapse:
            collapsed = self.collapse()
            return collapsed.getFunction(), 'FUNC'
        if len(self.missingArgs()) != 0:
            raise Exception("Not enough arguments provided")
        # Don't repeat work if we already have a value
        if self._value is not None:
            return self._value, self._outputType
        values = {}
        for k in self._inputBlocks:
            val = self._inputBlocks[k]
            if self._inputTypes[k] == 'FUNC':
                v,t = val.evaluate(collapse=True)
            else:
                v,t = val.evaluate()
            if t != self._inputTypes[k] and not (t is 'ANY' or self._inputTypes[k] is 'ANY' or t is 'FUNC' or self._inputTypes[k] is 'FUNC'):
                raise Exception("Argument type mismatch")
            values[k] = v
        self._value = self._func(*(values.values()))
        return self._value, self.getOutputType()

    def collapseNoMissingArgs(self):
        val, valType = self.evaluate()
        block = InputBlock()
        block._type = valType
        block.add(val)
        return block

    def collapseWithMissingArgs(self, missingArgs, parentsCollapsed):
        block = FunctionBlock()
        block._outputType = self.getOutputType()
        parentsInfo = {k: {'func': parent.getFunction(), 'inputs': parent._inputTypes} for k, parent in parentsCollapsed.items()}
        # Get a mapping from function to parent inputs
        flattenedTypes = []
        missingArgsMapped = [self._inputTypes[k] for k in missingArgs]
        for parentInfo in parentsInfo.values():
            flattenedTypes += [inputType for inputType in parentInfo['inputs'].values()]
        remap = []
        for k in missingArgs:
            remap.insert(k, {'func': lambda value: value, 'inputsLen': 1})
        for k,v in parentsInfo.items():
            remap.insert(k, {'func': v['func'], 'inputsLen': len(v['inputs'])})
        cur = 0
        for i in xrange(len(remap)):
            length = remap[i]['inputsLen']
            remap[i]['inputsLen'] = (cur, cur+length)
            cur += length
        # if parents aren't missing args, flattenedTypes is []
        newInputTypes = flattenedTypes + missingArgsMapped
        block._inputTypes = {i : newInputTypes[i] for i in xrange(len(newInputTypes))}
        # Join the functions for parents needing args + our function if we need an arg.
        selfFunc = self._func
        block._func = Closure(lambda *args: selfFunc(*([l['func'](*[args[i] for i in xrange(l['inputsLen'][0], l['inputsLen'][1])]) for l in remap])))
        return block

    def collapse(self):
        missingArgs = self.missingArgs()
        if not self._collapsedCopy is None and self._collapsedCopyArgs == missingArgs:
            return self._collapsedCopy
        parentsCollapsed = {k: v.collapse() for k,v in self._inputBlocks.items() if not v is None}
        parentsMissingArgs = {k: parent.missingArgs() for k, parent in parentsCollapsed.items()}
        collapsed = None
        if all([len(args) == 0 for args in parentsMissingArgs.values()]):
            if len(missingArgs) == 0:
                self._collapsedCopy = self.collapseNoMissingArgs()
                self._collapsedCopyMissingArgs = missingArgs
                return self._collapsedCopy
        self._collapsedCopy = self.collapseWithMissingArgs(missingArgs, parentsCollapsed)
        self._collapsedCopyMissingArgs = missingArgs
        return self._collapsedCopy

class InputBlock(Block):
    _type = 'ARG'
    _func = lambda self: self._value

    def __init__(self, *args, **kwargs):
        self._outputType = 'ARG'
        self._func = Closure(self._func, self)
        if 'argType' in kwargs.keys():
            self._type = kwargs['argType']
        super(InputBlock, self).__init__(*args, **kwargs)

    def add(self, value):
        if not type(value) is TYPES[self._type]:
            raise Exception("Incorrect type: {value} does not have type {typeKey}"
                            .format(value=value, typeKey=self._type))
        self._value = value
        self._outputType = self._type

class FunctionBlock(Block):

    def __init__(self, *args, **kwargs):
        if 'outputType' in kwargs.keys():
            self.outputType = kwargs['outputType']
        super(FunctionBlock, self).__init__(*args, **kwargs)
        self._func = Closure(self._func)
