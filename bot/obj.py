# BOTLIB - the bot library !
#
#

import datetime, importlib, json, os, random, sys, time, _thread

def __dir__():
    return ("Cfg", "Default", "O", "Object", "ObjectEncoder", "ObjectDecoder")

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

    def __init__(self, *args, **kwargs):
        super().__init__()
        stime = str(datetime.datetime.now()).replace(" ", os.sep)
        self._path = os.path.join(get_type(self), stime)
        return self

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

    def get(self, k, d=None):
        return self.__dict__.get(k, d)

    def items(self):
        return self.__dict__.items()

    def json(self):
        return json.dumps(self, cls=ObjectEncoder, indent=4, sort_keys=True)

    def keys(self):
        return self.__dict__.keys()

    def merge(self, o, vals=["",]):
        return self.update(strip(o, vals))

    def set(self, k, v):
        self.__dict__[k] = v

    def update(self, d):
        return self.__dict__.update(d)
        
    def values(self):
        return self.__dict__.values()

class Object(O):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            try:
                self.update(args[0])
            except TypeError:
                self.update(vars(args[0]))
        if kwargs:
            self.update(kwargs)

    def __str__(self):
        return self.json()

    def edit(self, setter, skip=False):
        try:
            setter = vars(setter)
        except:
            pass
        if not setter:
            setter = {}
        count = 0
        for key, value in setter.items():
            if skip and value == "":
                continue
            count += 1
            if value in ["True", "true"]:
                self[key] = True
            elif value in ["False", "false"]:
                self[key] = False
            else:
                self[key] = value
        return count

    def find(self, val):
        for item in self.values():
            if val in item:
                return True
        return False

    def format(self, keys=None):
        if keys is None:
            keys = vars(self).keys()
        res = []
        txt = ""
        for key in keys:
            if key == "stamp":
                continue
            val = self.get(key, None)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append(val)
        for val in res:
            txt += "%s%s" % (val.strip(), " ")
        return txt.strip()

    def last(self, strip=False):
        from .dbs import Db
        db = Db()
        path, l = db.last_fn(str(get_type(self)))
        if l:
            if strip:
                self.update(strip(l))
            else:
                self.update(l)
            self._path = path

    @locked(lock)
    def load(self, path, force=False):
        assert path
        assert workdir
        lpath = os.path.join(workdir, "store", path)
        if not os.path.exists(lpath):
            cdir(lpath)
        self._path = path
        with open(lpath, "r") as ofile:
            try:
                val = json.load(ofile, cls=ObjectDecoder)
            except json.decoder.JSONDecodeError as ex:
                raise EJSON(str(ex) + " " + lpath)
            if not val:
                raise EJSON("failed %s" % lpath)
            try:
                del val.__dict__["stamp"]
            except KeyError:
                pass
            self.update(val.__dict__)
        return self

    def register(self, k, v):
        self[k] = v

    @locked(lock)
    def save(self, stime=None):
        assert workdir
        if stime:
            self._path = os.path.join(get_type(self), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, sort_keys=True)
        return self._path

    def search(self, match=None):
        res = False
        if match == None:
            return res
        for key, value in match.items():
            val = self.get(key, None)
            if val:
                if not value:
                    res = True
                    continue
                if value in str(val):
                    res = True
                    continue
                else:
                    res = False
                    break
            else:
                res = False
                break
        return res

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

def stamp(o):
    for k in dir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def strip(o, vals=["",]):
    rip = []
    for k in o:
        value = o.get(k, None)
        for v in vals:
            if value == v:
                rip.append(k)
    for k in rip:
        del o[k]
    return o
