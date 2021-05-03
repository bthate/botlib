# This file is placed in the Public Domain.

import os
import sys

#sys.path.insert(0, "bot")

from cmn import spl
from dbs import last
from obj import Default, Object, fmt
from nms import Names
from prs import parseargs
from thr import launch

import adm
import bus
import clk
import dbs
import edt
import evt
import fnd
import hdl
import irc
import log
import nms
import obj
import opt
import prs
import rss
import slg
import tdo
import udp

class Kernel(Object):

    kernels = []

    table = Object()
    table.adm = adm
    table.bus = bus
    table.clk = clk
    table.dbs = dbs
    table.edt = edt
    table.evt = evt
    table.fnd = fnd
    table.hdl = hdl
    table.irc = irc
    table.log = log
    table.nms = nms
    table.obj = obj
    table.opt = opt
    table.prs = prs
    table.slg = slg
    table.rss = rss
    table.tdo = tdo
    table.udp = udp

    def __init__(self):
        super().__init__()
        self.kernels.append(self)

    def boot(self, name, version, wd):
        from obj import cfg
        cfg.wd = wd
        last(cfg)
        cfg.name = name
        cfg.version = version
        if len(sys.argv) > 1:
            parseargs(cfg, " ".join(sys.argv[1:]))
            if cfg.sets:
                cfg.changed = True
                cfg.update(cfg.sets)
            if cfg.opts:
                cfg.changed = True
                cfg.opts.update(cfg.opts)
        print(fmt(cfg))
        self.regs(cfg.mods)

    def cmd(self, txt):
        self.prompt = False
        e = self.event(txt)
        docmd(self, e)
        e.wait()
        return e
            
    @staticmethod
    def getcmd(c):
        mn = Names.getmodule(c)
        mod = Kernel.table.get(mn, None)
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

    def first(self):
        if Kernel.kernels:
            return Kernel.kernels[0]
