# BOTLIB - the bot library !
#
#

__version__ = 87

## imports

import inspect, os, sys, threading, time, _thread

from .obj import Cfg, Db, Object
from .flt import Fleet
from .hdl import Event, Handler
from .thr import Launcher
from .utl import elapsed
from .usr import Users

## defines


starttime = time.time()

## classes

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

## runtime

k = Kernel()

def get_kernel():
    return k
