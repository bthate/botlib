# This file is placed in the Public Domain.

"database,timer and tables"

import datetime
import os
import queue
import sys
import time
import threading
import types

from .hdl import launch, parse_txt
from .obj import Default, Object, cfg, spl, getname, gettype, search

def __dir__():
    return ('Cfg', 'Kernel', 'Repeater', 'Timer', 'all', 'debug', 'deleted',
            'every', 'find', 'fns', 'fntime', 'hook', 'last', 'lastfn',
            'lastmatch', 'lasttype', 'listfiles')

all = "adm,cms,fnd,irc,krn,log,rss,tdo"

class ENOTYPE(Exception):

    pass

class Cfg(Default):

    pass

class Kernel(Object):

    cfg = Cfg()
    cmds = Object()
    fulls = Object()
    names = Default()
    modules = Object()
    table = Object()

    @staticmethod
    def addcmd(func):
        n = func.__name__
        Kernel.modules[n] = func.__module__
        Kernel.cmds[n] = func

    @staticmethod
    def addcls(cls):
        n = cls.__name__.lower()
        if n not in Kernel.names:
            Kernel.names[n] = []
        nn = "%s.%s" % (cls.__module__, cls.__name__)
        if nn not in Kernel.names[n]:
            Kernel.names[n].append(nn)

    @staticmethod
    def addmod(mod):
        n = mod.__spec__.name
        Kernel.fulls[n.split(".")[-1]] = n
        Kernel.table[n] = mod

    @staticmethod
    def boot(name, mods=None):
        if mods is None:
            mods = ""
        Kernel.cfg.name = name
        parse_txt(Kernel.cfg, " ".join(sys.argv[1:]))
        if Kernel.cfg.sets:
            Kernel.cfg.update(Kernel.cfg.sets)
        Kernel.cfg.save()
        Kernel.regs(mods or "irc,adm")

    @staticmethod
    def getcls(name):
        if "." in name:
            mn, clsn = name.rsplit(".", 1)
        else:
            raise ENOCLASS(fullname) from ex
        mod = Kernel.getmod(mn)
        return getattr(mod, clsn, None)

    @staticmethod
    def getcmd(c):
        return Kernel.cmds.get(c, None)

    @staticmethod
    def getfull(c):
        return Kernel.fulls.get(c, None)

    @staticmethod
    def getmod(mn):
        return Kernel.table.get(mn, None)

    @staticmethod
    def getnames(nm, dft=None):
        return Kernel.names.get(nm, dft)

    @staticmethod
    def getmodule(mn, dft):
        return Kernel.modules.get(mn ,dft)

    @staticmethod
    def init(mns):
        for mn in spl(mns):
            mnn = Kernel.getfull(mn)
            mod = Kernel.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init)

    @staticmethod
    def opts(ops):
        for opt in ops:
            if opt in Kernel.cfg.opts:
                return True
        return False

    @staticmethod
    def regs(mns):
        for mn in spl(mns):
            mnn = Kernel.getfull(mn)
            mod = Kernel.getmod(mnn)
            if "register" in dir(mod):
                mod.register(Kernel)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

def kcmd(hdl, obj):
    obj.parse()
    f = Kernel.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    sys.stdout.flush()
    obj.ready()

# timer

class Timer(Object):

    def __init__(self, sleep, func, *args, name=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = name or  ""
        self.state = Object()
        self.timer = None

    def run(self):
        self.state.latest = time.time()
        launch(self.func, *self.args)

    def start(self):
        if not self.name:
            self.name = getname(self.func)
        timer = threading.Timer(self.sleep, self.run)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self):
        thr = launch(self.start)
        super().run()
        return thr

# database

def all(otype, selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    otypes = Kernel.getnames(otype, [])
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def deleted(otype):
    otypes = Kernel.getnames(otype, [])
    for t in otypes:
        for fn in fns(t):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

def every(selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    for otype in os.listdir(os.path.join(cfg.wd, "store")):
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def find(otype, selector=None, index=None, timed=None):
    if selector is None:
        selector = {}
    got = False
    nr = -1
    otypes = Kernel.getnames(otype, [])
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
    if not got:
        return (None, None)

def last(o):
    path, l = lastfn(str(gettype(o)))
    if  l:
        o.update(l)
    if path:
        spl = path.split(os.sep)
        stp = os.sep.join(spl[-4:])
        return stp

def lastmatch(otype, selector=None, index=None, timed=None):
    res = sorted(find(otype, selector, index, timed), key=lambda x: fntime(x[0]))
    if res:
        return res[-1]
    return (None, None)

def lasttype(otype):
    fnn = fns(otype)
    if fnn:
        return hook(fnn[-1])

def lastfn(otype):
    fn = fns(otype)
    if fn:
        fnn = fn[-1]
        return (fnn, hook(fnn))
    return (None, None)

def fns(name, timed=None):
    if not name:
        return []
    p = os.path.join(cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if timed and "from" in timed and timed["from"] and fntime(p) < timed["from"]:
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)

def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t

def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    t = Kernel.getcls(cname)
    if not t:
        raise ENOTYPE(cname)
    if fn:
        o = t()
        o.load(fn)
        return o
    else:
        raise ENOTYPE(cname)

def listfiles(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))
