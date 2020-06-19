# BOTLIB - the bot library !
#
#

import sys, threading

from .utl.shl import setcompleter
from .utl.thr import launch
from .krn import k
from .obj import Cfg, Object
from .hdl import Event, Handler
from .tbl import names

class Cfg(Cfg):

    pass

class Console(Object):

    def  __init__(self):
        super().__init__()
        self.cfg = Cfg()
        k.fleet.add(self)

    def announce(self, txt):
        self.raw(txt)

    def input(self):
        while 1:
            e = self.poll()
            if not e:
                break
            k.dispatch(e)

    def poll(self):
        txt = input("> ")
        e = Event()
        e.parse(txt)
        e.orig = repr(self)
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self, cfg):
        if cfg:
            self.cfg.update(cfg)
        else:
            self.cfg.last()
        setcompleter(names)
        launch(self.input)
