# BOTLIB - the bot library !
#
#

""" objects to save to disk. """

import datetime, json, os, time

from .utl import get_type, hooked

workdir = ""

## classes

class Object:

    """ base Object to inherit from, provides a __stamp__ hidden attribute to load/save from. """

    __slots__ = ("__dict__", "__stamp__")

    def __init__(self, *args, **kwargs):
        """ create object and set __stamp__. """
        super().__init__()
        if args:
            try:
                update(self, args[0])
            except TypeError:
                update(self, vars(args[0]))
        if kwargs:
            update(self, kwargs)
        self.__stamp__ = os.path.join(get_type(self), str(datetime.datetime.now()).replace(" ", os.sep))

    def __delitem__(self, k):
        """ remove item. """
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        """ return item, use None as default. """
        return self.__dict__.get(k, d)

    def __iter__(self):
        """ iterate over the keys. """
        return iter(self.__dict__.keys())

    def __len__(self):
        """ determine length of this object. """
        return len(self.__dict__)

    def __lt__(self, o):
        """ check for lesser than. """
        return len(self) < len(o)

    def __setitem__(self, k, v):
        """ set item to value and return reference to it. """
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        """ return a 4 space indented json string. """
        return json.dumps(self, cls=ObjectEncoder)

class ObjectEncoder(json.JSONEncoder):

    """ encode an Object to string. """

    def default(self, o):
        """ return string for object. """
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        return repr(o)

class ObjectDecoder(json.JSONDecoder):

    """ decode an Object from string. """

    def decode(self, o):
        """ return object from string. """
        return json.loads(o, object_hook=hooked)

class Ol(Object):

    """ object list. """

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

def load(o, path, force=False):
    """ load an object from json file at the provided path. """
    assert path
    assert workdir
    o.__stamp__ = path
    lpath = os.path.join(workdir, "store", path)
    cdir(lpath)
    with open(lpath, "r") as ofile:
        val = json.load(ofile, cls=ObjectDecoder)
        if val:
            if isinstance(val, Object):
                self.__dict__.update(vars(val))
            else:
                self.__dict__.update(val)

def names(name, timed=None):
    """ return filenames in the working directory. """
    if not name:
        return []
    assert workdir
    p = os.path.join(workdir, "store", name) + os.sep
    res = []
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(workdir, "store"))[-1]
            ftime = fntime(fnn)
            if timed and "from" in timed and timed["from"] and ftime < timed["from"]:
                continue
            if timed and timed.to and ftime > timed.to:
                continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

def save(o, stime=None):
    """ save this object to a json file, uses the hidden attribute __stamp__. """
    assert workdir
    if stime:
        o.__stamp__ = os.path.join(get_type(o), stime) + "." + str(random.randint(1, 100000))
    opath = os.path.join(workdir, "store", o.__stamp__)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(stamp(o), ofile, cls=ObjectEncoder)
    return o.__stamp__

def update(o, d):
    """ update an object with provided dict. """
    if isinstance(d, Object):
        return o.__dict__.update(vars(d))
    return o.__dict__.update(d)

def find(self, txt):
    for k, v in self.items():
        if txt in str(v):
            return True
    return False

def format(o, keys=None, pure=False, skip=[]):
    if not keys:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if skip and key in skip:
            continue
        if key == "stamp":
            continue
        try:
            val = o[key]
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

def get(o, k, d=None):
    return o.__dict__.get(k, d)

def items(o):
    return o.__dict__.items()

def keys(o):
    return o.__dict__.keys()

def update(o, d):
    if isinstance(d, Object):
        return o.__dict__.update(vars(d))
    return o.__dict__.update(d)

def values(o):
    return o.__dict__.values()

def find(o, txt):
    for k, v in o.items():
        if txt in str(v):
            return True
    return False

def format(o, keys=None, pure=False, skip=[]):
    if not keys:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if skip and key in skip:
            continue
        if key == "stamp":
            continue
        try:
            val = o[key]
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
