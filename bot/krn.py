# This file is placed in the Public Domain.

import obj
import os
import sys
import time

from cmn import spl
from dbs import last
from ldr import Loader
from obj import Cfg, Default, Object, fmt
from nms import Names
from prs import parseargs
from run import kernels
from thr import launch

all = "adm,fnd,log,tdo,irc,rss,slg,udp"
min = "cms,irc"

class Cfg(Cfg):

    pass

class Kernel(Loader):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        kernels.append(self)

    def boot(self, name, version):
        if len(sys.argv) <= 1:
            return
        self.starttime = time.time()
        self.cfg.name = name
        self.cfg.version = version
        parseargs(self.cfg, " ".join(sys.argv[1:]))
        self.cfg.save()
        if "all" in self.cfg.mods:
            m = all
        else:
            m = self.cfg.mods + min
        self.regs(m)

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
        return self.table.get(mn, None)

    def regs(self, mns):
        for mn in spl(mns):
            mod = self.mod(mn)
            if mod and "register" in dir(mod):
                mod.register()
