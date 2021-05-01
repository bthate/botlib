# This file is placed in the Public Domain.

import os
import sys

from cmn import spl
from obj import Object, cfg
from nms import Names
from prs import parseargs
from thr import launch

all = ["bus", "clk", "dbs", "edt", "evt", "hdl", "irc", "nms", "obj", "opt", "prs", "adm", "fnd", "log", "tdo", "rss", "udp"]

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

    @staticmethod
    def boot(wd=None, tbl=None):
        if tbl:
            Names.tbl(tbl)
        if len(sys.argv) >= 1:
            parseargs(cfg, " ".join(sys.argv[1:]))
            cfg.update(cfg.sets)
        cfg.name = sys.argv[0].split(os.sep)[-1]
        cfg.wd = wd or cfg.wd or os.path.expanduser("~/.%s" % cfg.name)

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
