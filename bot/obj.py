# BOTLIB - the bot library !
#
#

import datetime, importlib, json, os, random, sys, time, _thread

from .fil import cdir

lock = _thread.allocate_lock()
starttime = time.time()
workdir = ""

class ENOCLASS(Exception): pass

class ENOFILE(Exception): pass

class EJSON(Exception): pass

def locked(lock):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res
        return lockedfunc
    return lockeddec


class ObjectEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if type(o) in [str, True, False, int, float]:
            return o
        return repr(o)

class ObjectDecoder(json.JSONDecoder):

    def decode(self, s):
        return json.loads(s, object_hook=hooked)

class O:

    __slots__ = ("__dict__", "_path")

    def __init__(self):
        super().__init__()
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self._path = os.path.join(get_type(self), stime)

    def __delitem__(self, k):
        del self.__dict__[k]
        
    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        return self.json()

    def json(self):
        return json.dumps(self, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

    def get(self, k, d=None):
        return self.__dict__.get(k, d)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def merge(self, o, vals=["",]):
        return self.update(strip(o, vals))

    def register(self, k, v):
        self.__dict__[k] = v

    def set(self, k, v):
        self.__dict__[k] = v

    def update(self, d):
        self.__dict__.update(d)

    def values(self):
        return self.__dict__.values()

class Object(O):

    @locked(lock)
    def load(self, path, force=False):
        assert path
        assert workdir
        lpath = os.path.join(workdir, "store", path)
        if not os.path.exists(lpath):
            cdir(lpath)
        self._path = path
        with open(lpath, "r") as ofile:
            val = json.load(ofile, cls=ObjectDecoder)
            if val:
                self.update(val)
        return self

    @locked(lock)
    def save(self, stime=None):
        assert workdir
        if stime:
            self._path = os.path.join(get_type(self), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, skipkeys=True,sort_keys=True)
        return self._path


class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            self.__dict__.__setitem__(k, "")
        return self.__dict__[k]


class Cfg(Default):

    pass

class DoL(Object):

    def append(self, key, value):
        if key not in self:
            self[key] = []
        if type(value) == list:
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)

class List(Object):

    def __init__(self, txt):
        super().__init__()
        nr = 0
        for l in txt.split():
            if l:
                self[str(nr)] = arg(l)
                nr += 1

    def __iter__(self):
        for nr in range(len(self)):
            if type(nr) == int:
                try:
                    yield self[str(nr)]
                except KeyError:
                    pass

class Db(Object):

    def all(self, otype, selector={}, index=None, delta=0):
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            nr += 1
            if index is not None and nr != index:
                continue
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            yield o

    def deleted(self, otype, selector={}):
        nr = -1
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if selector and not o.search(selector):
                continue
            if "_deleted" not in o or not o._deleted:
                continue
            yield o
        
    def find(self, otype, selector={}, index=None, delta=0):
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if o.search(selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def find_value(self, otype, value, index=None, delta=0):
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            if o.find(value):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def last(self, otype, index=None, delta=0):
        fns = names(otype, delta)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_fn(self, otype, index=None, delta=0):
        fns = names(otype, delta)
        if fns:
            fn = fns[-1]
            return (fn, hook(fn))
        return (None, None)

    def last_all(self, otype, selector={}, index=None, delta=0):
        nr = -1
        res = []
        for fn in names(otype, delta):
            o = hook(fn)
            if selector and o.search(selector):
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

def fntime(daystr):
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

def get_cls(name):
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
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        o.update(d)
        return o

def last(o, strip=False):
    db = Db()
    path, l = db.last_fn(str(get_type(o)))
    if l:
        if strip:
            o.update(strip(l))
        else:
            o.update(l)
        o._path = path

def names(name, delta=None):
    if not name:
        return []
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

def stamp(o):
    for k in xdir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def strip(o):
    for k in o:
       if not k:
          del o[k]
    return o

def xdir(o, skip=""):
    res = []
    for k in dir(o):
        if skip and skip in k:
            continue
        res.append(k)
    return res
