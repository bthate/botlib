# BOTLIB - the bot library !
#
# core data.

import inspect, bot.obj, os, sys, threading, time, _thread

from .obj import Cfg, Object
from .dbs import Db
from .flt import Fleet
from .hdl import Command, Handler
from .tms import elapsed
from .trc import get_exception
from .usr import Users

def __dir__():
    return ("Cfg", "Kernel")

starttime = time.time()

class Cfg(Cfg):

    pass

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._prompted = threading.Event()
        self._prompted.set()
        self._ready = threading.Event()
        self._started = False
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        self.workdir = bot.obj.workdir
        self.fleet.add(self)
        kernels.append(self)
        self.register("command", dispatch)

    def announce(self, txt):
        pass
        
    def add(self, cmd, func):
        self.cmds[cmd] = func

    def init(self, mns):
        if not mns:
            return []
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            try:
                mod = self.load_mod("bot.%s" % mn)
            except ModuleNotFoundError:
                mod = self.load_mod(mn)
            if mod and "init" in dir(mod):
                mods.append(mod.init(self))
        return mods

    def start(self):
        self.users.oper(self.cfg.owner)
        super().start()
        self.init(self.cfg.modules)
            
    def ready(self):
        self._ready.set()

    def say(self, channel, txt):
        print(txt)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        self._ready.wait()

