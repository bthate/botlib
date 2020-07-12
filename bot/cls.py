# BOTLIB - the bot library
#
#

from .obj import Object

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            return ""
        return self.__dict__[k]

class Dict(Object):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            try:
                self.update(args[0])
            except TypeError:
                self.update(vars(args[0]))
        if kwargs:
            self.update(kwargs)

    def get(self, k, d=None):
        return self.__dict__.get(k, d)

    def update(self, d):
        if isinstance(d, Object):
            return self.__dict__.update(vars(d))
        return self.__dict__.update(d)


class DoL(Object):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if isinstance(value, type(list)):
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)
