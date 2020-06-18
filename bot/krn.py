# BOTLIB - the bot library !
#
#

__version__ = 87

import inspect, os, sys, threading, time, traceback, _thread

from .obj import Cfg, Db, Object
from .flt import Fleet
from .hdl import Event, Handler
from .thr import Launcher
from .utl import elapsed
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

def direct(name):
    return importlib.import_module(name)

def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        if fname.endswith(".py"):
            plugfile = fname[:-3].split(os.sep)
        else:
            plugfile = fname.split(os.sep)
        mod = []
        for element in plugfile[::-1]:
            mod.append(element)
            if "ok" in element:
                break
        ownname = ".".join(mod[::-1])
        result.append("%s:%s" % (ownname, linenr))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

k = Kernel()

def get_kernel():
    return k
