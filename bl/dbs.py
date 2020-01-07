# BOTLIB - Framework to program bots (a botlib).
#
# databases. 

import os
import time
import _thread
import bl

from bl.err import ENOFILE
from bl.obj import Object
from bl.tms import fntime
from bl.typ import get_cls
from bl.utl import locked

# defines

def __dir__():
    return ("Db", "find", "hook", "lock", "names")

lock = _thread.allocate_lock()

# classes

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

    def last(self, otype, index=None, delta=0):
        fns = names(otype, delta)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_all(self, otype, selector={}, index=None, delta=0):
        res = []
        nr = -1
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

# functions

def find(event):
    opts = os.listdir(os.path.join(k.cfg.workdir, "store"))
    try:
        match = event.txt.split(" ")[1]
    except (IndexError, AttributeError):
        event.reply("find %s" % "|".join([x.split(".")[-1].lower() for x in opts]))
        return
    opts = [x for x in opts if match in x.lower()]
    c = 0
    db = Db()
    for opt in opts:
        if len(event.txt.split()) > 2:
           for arg in event.txt.split()[2:]:
               selector = {arg: ""}
        else:
            selector = {"txt": ""}
        for o in db.find(opt, selector):
            event.display(o, str(c))
            c += 1

@locked(lock)
def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def names(name, delta=None):
    assert bl.obj.workdir
    if not name:
        return []
    p = os.path.join(bl.obj.workdir, "store", name) + os.sep
    res = []
    now = time.time()
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=True):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(bl.obj.workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

# runtime

k = kernels.get("0", None)
