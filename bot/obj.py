# BOTLIB - the bot library !
#
#

""" objects to save to disk. """

import datetime, json, os, sys, random, time

## defines

workdir = None

def locked(l):
    """ lock on provided lock. """
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockedfunc.__doc__ = func.__doc__
        return lockedfunc
    return lockeddec

## classes

class Object:

    """ base Object to inherit from, provides a __stamp__ hidden attribute to load/save from. """

    __slots__ = ("__dict__", "__stamp__")

    def __init__(self):
        """ create object and set __stamp__. """
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

    def load(self, path, force=False):
        """ load an object from json file at the provided path. """
        assert path
        assert workdir
        self.__stamp__ = path
        lpath = os.path.join(workdir, "store", path)
        cdir(lpath)
        with open(lpath, "r") as ofile:
            val = json.load(ofile, cls=ObjectDecoder)
            if val:
                if isinstance(val, Object):
                    self.__dict__.update(vars(val))
                else:
                    self.__dict__.update(val)

    def save(self, stime=None):
        """ save this object to a json file, uses the hidden attribute __stamp__. """
        assert workdir
        if stime:
            self.__stamp__ = os.path.join(get_type(self), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self.__stamp__)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder)
        return self.__stamp__

class Db(Object):

    """ database interface to Objects stored on disk. """

    def all(self, otype):
        """ return all objects of a type. """
        nr = -1
        if selector is None:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            yield o

    def deleted(self, otype):
        """ show all deleted records of a type. """
        nr = -1
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if "_deleted" not in o or not o._deleted:
                continue
            yield o

    def find(self, otype, selector=None, index=None, delta=0):
        """ find all objects of a type matching fields in the provided selector. """
        nr = -1
        if selector is None:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            if search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def find_value(self, otype, value, index=None, delta=0):
        """ find object that have values that matches provided string. """
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if o.find(value):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def last(self, otype):
        """ return last saved object of a type. """
        fns = names(otype)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_fn(self, otype):
        """ return filename of last saved object of a type. """
        fns = names(otype)
        if fns:
            fn = fns[-1]
            return (fn, hook(fn))
        return (None, None)

    def last_all(self, otype, selector=None):
        """ return the last object of a type matching the selector. """
        nr = -1
        res = []
        if not selector:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            if selector is not None and search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                res.append((fn, o))
            else:
                res.append((fn, o))
        if res:
            s = sorted(res, key=lambda x: fntime(x[0]))
            if s:
                return s[-1][-1]
        return None

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

## utilities

def cdir(path):
    """ create directory. """
    if os.path.exists(path):
        return
    res = ""
    path2, fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass
    return True

def fntime(daystr):
    """ return time from filename. """
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    try:
        datestr, rest = datestr.rsplit(".", 1)
    except ValueError:
        rest = ""
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            t += float("." + rest)
    except ValueError:
        t = 0
    return t

def get(o, k, d=None):
    return o.__dict__.get(k, d)

def get_cls(name):
    """ return class by full qualified name. """
    try:
        modname, clsname = name.rsplit(".", 1)
    except:
        raise ENOCLASS(name)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_type(o):
    """ return type of an object. """
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def hook(fn):
    """ return object from filename. """
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILENAME(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def hooked(d):
    """ convert to object depending on filename stamp. """
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        update(o, d)
        return o
    return d

def last(o):
    """ update object in place with the last saved version. """
    db = Db()
    path, l = db.last_fn(str(get_type(o)))
    if  l:
        o.update(l)
        o.__stamp__ = path

def names(name, delta=None):
    """ return filenames in the working directory. """
    if not name:
        return []
    assert workdir
    p = os.path.join(workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if delta:
        past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

def search(o, selector=None):
    """ search objects that match provided selector. """
    res = False
    if selector is None:
        selector = {}
    for key, value in selector.items():
        try:
            val = o[key]
        except KeyError:
            continue
        if val:
            if not value:
                res = True
                continue
            if value in str(val):
                res = True
                continue
            res = False
            break
    return res

def stamp(o):
    """ recursively add filename fields to a dict. """
    for k in xdir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo.__stamp__
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o.__stamp__
    return o

def update(o, d):
    """ update o with d. """
    if isinstance(d, Object):
        return o.__dict__.update(vars(d))
    return o.__dict__.update(d)

def xdir(o, skip=None):
    """ return dir() but skipping unwanted keys. """
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
