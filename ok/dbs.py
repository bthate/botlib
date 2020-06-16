# OKLIB - the ok library !
#
# databases.

import importlib, ok, os, sys, time

from .obj import Object, get_cls, hook

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

def names(name, delta=None):
    assert ok.obj.workdir
    if not name:
        return []
    p = os.path.join(ok.obj.workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if delta:
        past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(ok.obj.workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)
