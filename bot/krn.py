# BOTLIB - the bot library !
#
#

__version__ = 87

import inspect, os, sys, threading, time, traceback, _thread

from .obj import Cfg, Db, Object
from .flt import Fleet
from .hdl import Handler
from .thr import Launcher
from .utl import elapsed, get_exception
from .usr import Users

starttime = time.time()

class ENOKERNEL(Exception):

    pass

class Cfg(Cfg):

    pass

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
        from .evt import Event
        e = Event(txt)
        self.dispatch(e)
        return e

    def say(self, channel, txt):
        print(txt)

    def start(self, cfg={}):
        self.cfg.update(cfg)

    def stop(self):
        self._queue.put(None)

    def wait(self):
        while 1:
            time.sleep(1.0)

k = Kernel()

def get_kernel():
    return k
