# BOTLIB - the bot library !
#
#

import datetime, json, os, sys, time, _thread

from bot.err import ENOCLASS

lock = _thread.allocate_lock()
workdir = ""

def locked(l):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
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
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        return repr(o)

class ObjectDecoder(json.JSONDecoder):

    def decode(self, o):
        return json.loads(o, object_hook=hooked)

class Object:

    __slots__ = ("__dict__", "_path")

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            try:
                update(self, args[0])
            except TypeError:
                update(self, vars(args[0]))
        if kwargs:
            update(self, kwargs)
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self._path = os.path.join(get_type(self), stime)

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        return json.dumps(self, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

class Obj(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self["_path"] = os.path.join(get_type(self), stime)

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            return super().__getitem__(k)

    def __setattr__(self, k, v):
        self[k] = v

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            return ""
        return self.__dict__[k]

class Cfg(Default):

    pass

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

def cdir(path):
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

def edit(o, setter, skip=False):
    try:
        setter = vars(setter)
    except (TypeError, ValueError):
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        if skip and value == "":
            continue
        count += 1
        if value in ["True", "true"]:
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
    return count

def find(o, val):
    for item in o.values():
        if val in item:
            return True
    return False

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

def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    load(o, fn)
    return o

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        update(o, d)
        return o
    return d

def locked(l):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        return lockedfunc
    return lockeddec

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

def get(o, k, d=None):
    return o.__dict__.get(k, d)

def get_type(o):
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def items(o):
    return o.__dict__.items()

def keys(o):
    return o.__dict__.keys()

def last(o, strip=False):
    from .dbs import Db
    db = Db()
    path, l = db.last_fn(str(get_type(o)))
    if l:
        if strip:
            update(o, strip(l))
        else:
            update(o, l)
        o._path = path

@locked(lock)
def load(o, path, force=False):
    assert path
    assert workdir
    lpath = os.path.join(workdir, "store", path)
    if not os.path.exists(lpath):
        cdir(lpath)
    o._path = path
    with open(lpath, "r") as ofile:
        val = json.load(ofile, cls=ObjectDecoder)
        if val:
            update(o, val)

def merge(o, oo, vals=None):
    if vals is None:
        vals = ["",]
    return update(o, strip(oo, vals))

def register(o, k, v):
    o.__dict__[k] = v

@locked(lock)
def save(o, stime=None):
    assert workdir
    if stime:
        o._path = os.path.join(get_type(o), stime) + "." + str(random.randint(1, 100000))
    opath = os.path.join(workdir, "store", o._path)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(stamp(o), ofile, cls=ObjectEncoder, indent=4, skipkeys=True, sort_keys=True)
    return o._path

def set(o, k, v):
    o.__dict__[k] = v

def search(o, match=None):
    res = False
    if match is None:
        return res
    for key, value in match.items():
        val = get(o, key, None)
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

def slc(o, keys=None):
    res = type(o)()
    for k in o:
        if keys is not None and k in keys:
            continue
        res[k] = o[k]
    return res

def strip(o, skip=None):
    for k in o:
        if skip is not None and k in skip:
            continue
        if not k:
            del o[k]
    return o

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

def tojson(o):
    return json.dumps(o, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

def tostr(o, keys=None):
    if keys is None:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if key == "stamp":
            continue
        val = get(o, key, None)
        if not val:
            continue
        val = str(val)
        if key == "text":
            val = val.replace("\\n", "\n")
        res.append((key, val))
    for key, val in res:
        txt += "%s=%s%s" % (key, val.strip(), " ")
    return txt.strip()

def update(o, d):
    try:
        return o.__dict__.update(d)
    except (TypeError, ValueError):
        return o.__dict__.update(vars(d))

def values(o):
    return o.__dict__.values()

def xdir(o, skip=None):
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
