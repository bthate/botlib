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

def kcmd(hdl, obj):
    obj.parse()
    f = Kernel.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    sys.stdout.flush()
    obj.ready()

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
