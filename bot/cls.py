# BOTLIB - the bot library
#
#

from .obj import Db, Object, get_type

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

    def find(self, txt):
        for k, v in self.items():
            if txt in str(v):
                return True
        return False

    def format(self, keys=None, pure=False):
        if not keys:
            keys = vars(self).keys()
        res = []
        txt = ""
        for key in keys:
            if key == "stamp":
                continue
            try:
                val = self[key]
            except KeyError:
                continue
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append((key, val))
        for key, val in res:
            if pure:
                txt += "%s%s" % (val.strip(), " ")
            else:
                txt += "%s=%s%s" % (key, val.strip(), " ")
        return txt.strip()

    def get(self, k, d=None):
        return self.__dict__.get(k, d)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def last(self):
        db = Db()
        path, l = db.last_fn(str(get_type(self)))
        if l:
            self.update(l)
            self.__stamp__ = path

    def update(self, d):
        if isinstance(d, Object):
            return self.__dict__.update(vars(d))
        return self.__dict__.update(d)

    def values(self):
        return self.__dict__.values()

class Default(Dict):

    def __getattr__(self, k):
        if k not in self:
            return ""
        return self.__dict__[k]

class DoL(Dict):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if isinstance(value, type(list)):
            self[key].extend(value)
        else:
            if value not in self[key]:
                self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)
