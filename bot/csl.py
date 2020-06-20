# BOTLIB - the bot library !
#
#

import sys, threading

from .krn import k
from .obj import Cfg, Object
from .hdl import Event, Handler
from .shl import setcompleter
from .tbl import names
from .thr import launch

class Cfg(Cfg):

    pass

class Event(Event):

    def reply(self, txt):
        print(txt)

class Console(Object):

    def announce(self, txt):
        self.raw(txt)

    def input(self):
        while 1:
            event = self.poll()
            event.orig = repr(self)
            if not event:
                break
            k.put(event)
            event.wait()

    def poll(self):
        e = Event()
        e.parse(input("> "))
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        setcompleter(names)
        launch(self.input)
