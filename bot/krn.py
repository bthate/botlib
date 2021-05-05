# This file is placed in the Public Domain.

import os
import importlib
import importlib.util
import sys
import time

from .obj import Cfg, Default, Names, Object, fmt, last
from .prs import parse_txt
from .run import kernels
from .utl import launch

def spl(txt):
    return [x for x in txt.split(",") if x]

class Cfg(Cfg):

    pass

class Loader(Object):

    table = Object()

class Kernel(Loader):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.starttime = time.time()
        kernels.append(self)

    def boot(self, name, version):
        if len(sys.argv) <= 1:
            return
        self.starttime = time.time()
        self.cfg.name = name
        self.cfg.version = version
        parse_txt(self.cfg, " ".join(sys.argv[1:]))
        if self.cfg.sets:
            self.cfg.update(self.cfg.sets)
        self.cfg.save()
        self.regs(self.cfg.mods)

    def cmd(self, txt):
        self.prompt = False
        e = self.event(txt)
        docmd(self, e)
        e.wait()
        return e
            
    @staticmethod
    def getcmd(c):
        mn = Names.getmodule(c)
        mod = Loader.table.get(mn, None)
        return getattr(mod, c, None)

    def inits(self, mns):
        for mn in spl(mns):
            mod = self.mod(mn)
            if mod and "init" in dir(mod):
                launch(mod.init)

    def mod(self, mn):
        return Loader.table.get(mn, None)

    def regs(self, mns):
        for mn in spl(mns):
            mod = self.mod(mn)
            if mod and "register" in dir(mod):
                mod.register()

    def scan(self, path, name=""):
        if not os.path.exists(path):
            return
        if not name:
            name = path.split(os.sep)[-1]
        r = os.path.dirname(path)
        if r not in sys.path:
            sys.path.insert(0, r)
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            fqn = "%s.%s" % (name, mn)
            if not hasmod(fqn):
                continue
            self.load(fqn)
            
    def load(self, name):
        mod = importlib.import_module(name)
        Loader.table[name] = mod
        if "register" in dir(mod):
            mod.register()

def hasmod(fqn):
    try:
        spec = importlib.util.find_spec(fqn)
        if spec:
            return True
    except (ValueError, ModuleNotFoundError):
        pass
    return False

def mods(name):
    res = []
    if os.path.exists(name):
        for p in os.listdir(name):
            if p.startswith("__"):
                continue
            if p.endswith(".py"):
                res.append(p[:-3])
    return ",".join(res)

def privileges(name=None):
    if os.getuid() != 0:
        return
    if name is None:
        try:
            name = getpass.getuser()
        except KeyError:
            pass
    try:
        pwnam = pwd.getpwnam(name)
    except KeyError:
        return False
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    old_umask = os.umask(0o22)
    return True

def root():
    if os.geteuid() != 0:
        return False
    return True

