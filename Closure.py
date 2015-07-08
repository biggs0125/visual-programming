import cPickle
import new
import marshal

class ClosureObject(object):
    def __init__(self, obj, pickled):
        self.cell_contents = obj
        self.isPickled = pickled
        

class Closure(object):
    def __init__(self, func):
        self.func_code = marshal.dumps(func.func_code)
        self.func_name = func.func_name
        closure = func.func_closure
        self.func_closure = []
        for elem in closure:
            try:
                self.func_closure.append(ClosureObject(cPickle.dumps(elem.cell_contents), True))
            except TypeError:
                newDict = {}
                for k,obj in elem.cell_contents.items():
                    obj['func'] = Closure(obj['func'])
                    newDict[k] = obj
                self.func_closure.append(ClosureObject(newDict, False))

    def unfold(self):
        closure = []
        for elem in self.func_closure:
            if elem.isPickled:
                closure.append(cPickle.loads(elem.obj))
            else:
                newDict = {}
                for k,obj in elem.obj.items():
                    obj['func'] = obj['func'].unfold()
                    newDict[k] = obj
                closure.append(newDict)
        newClosure = tuple([self.make_cell(x) for x in closure])
        return new.function(marshal.loads(self.func_code), self.func_name, closure=newClosure)
    
    @staticmethod
    def make_cell(value):
        return (lambda x: lambda: x)(value).func_closure[0]
    
