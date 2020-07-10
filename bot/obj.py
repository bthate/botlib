# BOTLIB - the bot library !
#
#

import datetime, importlib, json, os, random, sys, time, types, _thread

from .utl import *

workdir = None

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
        self._path = os.path.join(get_type(self), str(datetime.datetime.now()).replace(" ", os.sep))

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        return self.__dict__.get(k, d)

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __len__(self):
        return len(self.__dict__)

    def __load__(self, path, force=False):
        assert path
        assert workdir
        self._path = path
        lpath = os.path.join(workdir, "store", path)
        cdir(lpath)
        with open(lpath, "r") as ofile:
            val = json.load(ofile, cls=ObjectDecoder)
            if val:
                self.update(val)

    def __save__(self, stime=None):
        assert workdir
        if stime:
            self._path = os.path.join(self.get_type(), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, skipkeys=True, sort_keys=True)
        return self._path

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        return json.dumps(self, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

def names(name, delta=None):
    from .utl import fntime
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
