# BOTLIB - the bot library !
#
#

__version__ = 97

import threading, time

from .cfg import Cfg
from .dft import Default
from .flt import Fleet
from .hdl import Handler
from .tsk import launch
from .trc import get_exception
from .usr import Users

def __dir__():
    return ("Cfg", "Kernel", "k")

starttime = time.time()

def spl(txt):
    return iter([x for x in txt.split(",") if x])

class Cfg(Default):

    def __init__(self):
        super().__init__()
        self.users = False

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = Cfg()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)

    def announce(self, txt):
        pass

    def init(self, mns):
        mods = []
        thrs = []
        for mn in spl(mns):
            ms = "bot.%s" % mn
            try:
                mod = self.load_mod(ms)
            except ModuleNotFoundError:
                try:
                    mod = self.load_mod(mn)
                except ModuleNotFoundError:
                    print(get_exception())
                    continue
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

k = Kernel()
