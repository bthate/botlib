# BOTLIB - Framework to program bots.
#
# 

__version__ = 72

workdir = ""

import logging
import time
import bl.cfg
import bl.csl
import bl.dbs
import bl.dpt
import bl.err
import bl.flt
import bl.hdl
import bl.typ
import bl.usr

from bl.obj import Object, get, set, update

def __dir__():
    return ("Cfg", "Kernel", "Object", "get", "set", "last", "update", "workdir", "k")

default = {
           "dosave": False,
           "doexec": False,
           "exclude": "",
           "kernel": False,
           "modules": "",
           "options": "",
           "owner": "",
           "prompting": True,
           "shell": False,
           "verbose": False
          }

class Cfg(bl.cfg.Cfg):

    pass

class Kernel(bl.hdl.Handler):

    cfg = Cfg(default)
    db = bl.dbs.Db()
    fleet = bl.flt.Fleet()
    users = bl.usr.Users()

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._started = False
        self.prompt = True
        self.state = bl.obj.Object()
        self.state.started = False
        self.state.starttime = time.time()
        self.verbose = True

    def add(self, bot):
        self.fleet.add(bot)

    def cmd(self, txt, origin=""):
        if not txt:
            return
        import bl.csl
        import bl.dpt
        self.cfg.prompting = False
        c = bl.csl.Console()
        c.start(False, False, False)
        e = bl.evt.Event()
        e.txt = txt
        e.options = self.cfg.options
        e.orig = repr(c)
        e.origin = origin or "root@shell"
        self.register(bl.dpt.dispatch)
        self.prompt = False
        self.add(c)
        self.handle(e)
        e.wait()

    def init(self, modstr):
        if not modstr:
            return
        ok = True
        for mod in get_mods(self, modstr):
            if "init" not in dir(mod):
                continue
            n = bl.utl.get_name(mod)
            if self.cfg.exclude and n in self.cfg.exclude.split(","):
                continue
            try:
                mod.init()
            except bl.err.EINIT as ex:
                if not self.cfg.doexec and not self.cfg.shell and not self.cfg.kernel:
                    print(str(ex))
                    ok = False
                    break
        return ok

    def start(self):
        if self._started:
            return
        self._started = True
        if self.cfg.doexec:
            self.init(self.cfg.modules)
            self.cmd(self.cfg.txt)
            return
        if self.cfg.owner:
            self.users.oper(self.cfg.owner)
        if self.cfg.kernel:
            bl.last(self.cfg)
        self.init(self.cfg.modules)
        self.register(bl.dpt.dispatch)
        super().start(True, False, False)

    def wait(self):
        if self.cfg.doexec:
            return
        if not self.cfg.kernel and self.cfg.dosave:
            self.cfg.save()
        if self.cfg.kernel or self.cfg.shell or (self.cfg.prompting and self.cfg.args):
            bl.shl.writepid()
            bl.shl.set_completer(self.cmds)
            bl.shl.enable_history()
            c = bl.csl.Console()
            c.start()
            while not self._stopped:
                time.sleep(1.0)

def get_mods(h, ms):
    modules = []
    for mn in ms.split(","):
        if not mn:
            continue
        m = None
        try:
            m = h.walk(mn)
        except ModuleNotFoundError as ex:
            pass
        if not m:
            try:
                m = h.walk("bl.%s" % mn)
            except ModuleNotFoundError as ex:
                pass
        if m:
            modules.extend(m)
    return modules

k = Kernel()

def last(o, skip=True):
    val = k.db.last(str(str(bl.typ.get_type(o))))
    if val:
        bl.obj.update(o, val)
        o.__path__ = val.__path__
        return o.__path__
