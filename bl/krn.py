# BOTLIB - Framework to program bots (a botlib).
#
# kernel for boot proces.

__version__ = 1

import logging
import time
import bl

from bl.err import EINIT
from bl.flt import Fleet
from bl.hdl import Event
from bl.ldr import Loader
from bl.obj import Cfg, Object
from bl.shl import enable_history, set_completer, writepid
from bl.thr import launch
from bl.trc import get_exception
from bl.usr import Users
from bl.utl import get_name

# defines

def __dir__():
    return ("Cfg", "Kernel", "Kernels", "kernels")

starttime = time.time()

# classes

class Cfg(Cfg):

    pass

class Kernel(Loader):

    cfg = Cfg()
    fleet = Fleet()
    users = Users()
        
    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self._skip = False
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        kernels.add(self)
        
    def cmd(self, txt, origin=""):
        if not txt:
            return
        from bl.csl import Console
        c = Console()
        e = Event()
        e.txt = txt
        e.origin = origin
        e.orig = repr(c)
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        if not event.txt:
            return
        event.parse()
        chk = event.txt.split()[0]
        try:
            event._func = self.get_cmd(chk)
        except Exception as ex:
            logging.error(get_exception())
            return
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def init(self, mns):
        mods = []
        for mod in self.walk(mns):
            if "init" in dir(mod):
                try:
                    mod.init(self)
                except EINIT as ex:
                    print(ex)
                    self._skip = True
                    return
                mods.append(mod)
        return mods

    def register(self, k, v):
        self.cmds.set(k, v)

    def start(self):
        if self._skip:
            return
        if self.cfg.kernel:
            self.cfg.last()
            self.cfg.shell = False
            self.cfg.prompting = False
            self._skip = False
        try:
            self.init(self.cfg.modules)
        except bl.err.EINIT as ex:
            print(ex)
            self._skip = True
            return
        if self.cfg.dosave:
            self.cfg.save()
        if self.cfg.shell:
            self.init("bl.csl")
        elif not self.cfg.kernel:
            self._skip = True

    def wait(self):
        if self._skip:
            return
        while not self._stopped:
            time.sleep(1.0)

class Kernels(Object):

    kernels = []
    nr = 0

    def add(self, kernel):
        logging.warning("add %s" % get_name(kernel))
        if kernel not in Kernels.kernels:
            Kernels.kernels.append(kernel)
            Kernels.nr += 1

    def get(self, nr, default=None):
        try:
            return Kernels.kernels[nr]
        except IndexError:
            pass

# runtime

kernels = Kernels()
