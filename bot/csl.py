# BOTLIB - the bot library !
#
#

__version__ = 1

## imports

import sys, threading

from .krn import k
from .obj import Object
from .hdl import Event, Handler
from .shl import setcompleter
from .tbl import names
from .thr import launch

## classes

class Console(Object):

    def announce(self, txt):
        self.raw(txt)

    def input(self):
        while 1:
            e = self.poll()
            if not e:
                break
            k.dispatch(e)

    def poll(self):
        return Event(input("> "))

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        setcompleter(names)
        launch(self.input)
