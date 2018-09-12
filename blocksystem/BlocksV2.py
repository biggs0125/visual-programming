class Block:
    _func = lambda: None
    _type = None
    _value = None
    
    def __init__(self, type):
        self._type = type
        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = self.__class__.__name__
