# BOTLIB - the bot library !
#
#

__version__ = 87

import inspect, os, sys, threading, time, traceback, _thread

from .utl.gnr import get_type
from .utl.tms import elapsed
from .utl.trc import get_exception
from .obj import Cfg, Db, Object
from .hdl import Handler
from .usr import Users

starttime = time.time()

class ENOKERNEL(Exception):

    pass

class Cfg(Cfg):

    pass

class Fleet(Object):

    bots = []

    def __iter__(self):
        return iter(Fleet.bots)

    def add(self, bot):
        Fleet.bots.append(bot)

    def announce(self, txt, skip=[]):
        for h in self.bots:
            if skip and type(h) in skip:
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        for b in Fleet.bots:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        for o in Fleet.bots:
            if repr(o) == orig:
                return o

    def by_cls(self, otype, default=None):
        res = []
        for o in Fleet.bots:
            if isinstance(o, otype):
                res.append(o)
        return res

    def by_type(self, otype):
        res = []
        for o in Fleet.bots:
            if otype.lower() in str(type(o)).lower():
                res.append(o)
        return res

    def say(self, orig, channel, txt):
        for o in Fleet.bots:
            if repr(o) == orig:
                o.say(channel, str(txt))

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)
        
    def cmd(self, txt):
        if not txt:
            return
        e = Event()
        e.parse(txt)
        e.orig = repr(self)
        self.dispatch(e)
        return e

    def say(self, channel, txt):
        print(txt)

    def start(self, cfg={}):
        self.cfg.update(cfg)

    def stop(self):
        self.queue.put(None)

    def wait(self):
        while 1:
            time.sleep(1.0)

k = Kernel()

def get_kernel():
    return k
