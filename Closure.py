import cPickle
import new
import marshal

class ClosureObject(object):
    def __init__(self, obj, pickled):
        self.cell_contents = obj
        self.isPickled = pickled
        

class Closure(object):
    def __init__(self, func):
        self.folded = False
        if '__builtins__' in func.func_globals:
            for k,v in func.func_globals['__builtins__'].items():
                try:
                    cPickle.dumps(v)
                except:
                    del func.func_globals['__builtins__'][k]
        self.func_globals = func.func_globals
        self.func_defaults = func.func_defaults
        self.func_code = marshal.dumps(func.func_code)
        self.func_name = func.func_name
        self.func_closure = func.func_closure
        
    def fold(self):
        if self.folded or self.func_closure is None:
            return
        closure = self.func_closure
        self.func_closure = []
        for elem in closure:
            try:
                self.func_closure.append(ClosureObject(cPickle.dumps(elem.cell_contents), True))
            except TypeError as e:
                newDict = {}
                for k,obj in elem.cell_contents.items():
                    obj['func'] = Closure(obj['func'])
                    obj['func'].fold()
                newDict[k] = obj
                self.func_closure.append(ClosureObject(newDict, False))
        self.folded = True

    def unfold(self):
        if not self.folded or self.func_closure is None:
            return
        closure = []
        for elem in self.func_closure:
            if elem.isPickled:
                closure.append(cPickle.loads(elem.cell_contents))
            else:
                newDict = {}
                for k,obj in elem.cell_contents.items():
                    obj['func'] = obj['func'].unfold()
                    newDict[k] = obj
                closure.append(newDict)
        newClosure = tuple([self.make_cell(x) for x in closure])
        self.func_closure = newClosure
        self.folded = False

    @staticmethod
    def make_cell(value):
        return (lambda x: lambda: x)(value).func_closure[0]
    
    def __call__(self, *args):
        if self.folded:
            self.unfold()
        return new.function(marshal.loads(self.func_code), self.func_globals, self.func_name, self.func_defaults, self.func_closure)(*args)
