# BOTLIB - the bot library !
#
#

from .obj import Object, names
from .utl import fntime, get_type, hook, update

def __init__():
    return ("Db",)

class Db(Object):

    def all(self, otype, selector=None, index=None, delta=0):
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

    def deleted(self, otype, selector=None):
        nr = -1
        if selector is None:
            selector = {}
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if selector and not search(o, selector):
                continue
            if "_deleted" not in o or not o._deleted:
                continue
            yield o

    def find(self, otype, selector=None, index=None, delta=0):
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

    def last_all(self, otype, selector=None, index=None, delta=0):
        nr = -1
        res = []
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

def last(o):
    db = Db()
    path, l = db.last_fn(str(get_type(o)))
    if  l:
        update(o, l)
        o._path = path

def search(o, match=None):
    res = False
    if match is None:
        return res
    for key, value in match.items():
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
