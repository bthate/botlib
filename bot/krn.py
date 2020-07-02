# BOTLIB - the bot library !
#
#

__version__ = 87

import threading, time

from .flt import Fleet
from .gnr import save
from .hdl import Handler
from .obj import Cfg, Object
from .thr import launch
from .usr import Users
from .utl import spl

def __dir__():
    return ("Cfg", "Kernel", "k")

class Cfg(Cfg):

    pass

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = Cfg()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)

    def init(self, mns):
        mods = []
        thrs = []
        for mn in spl(mns):
            ms = "bot.%s" % mn
            mod = self.load_mod(ms)
            mods.append(mod)
            func = getattr(mod, "init", None)
            if func:
                thrs.append(launch(func, self))
        for thr in thrs:
            thr.join()
        return mods

    def say(self, channel, txt):
        print(txt)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def wait(self):
        while not self.stopped:
            time.sleep(60.0)
