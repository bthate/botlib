# BOTLIB - the bot library !
#
#

import sys, threading

from .krn import k
from .obj import Cfg, Object
from .prs import parse
from .hdl import Event, Handler
from .shl import setcompleter
from .thr import launch

class Cfg(Cfg):

    pass

class Console(Object):

    def announce(self, txt):
        pass

    def input(self):
        while 1:
            event = self.poll()
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()

    def poll(self):
        e = Event()
        e.txt = input("> ")
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        setcompleter(k.cmds)
        launch(self.input)
