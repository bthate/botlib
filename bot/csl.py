# OKLIB - the ok library !
#
# console.

import sys, threading

from .krn import dispatch, get_kernel
from .hdl import Command, Loader
from .shl import setcompleter
from .thr import launch

def __dir__():
    return ("Console", "init")

def init(k):
    c = Console()
    c.cmds.update(k.cmds)
    c.start()
    return c

k = get_kernel()

class Command(Command):

    def show(self):
        for txt in self._result:
            print(txt)

class Console(Loader):

    def __init__(self):
        super().__init__()
        self._stopped = False
        k.fleet.add(self)
        
    def announce(self, txt):
        self.raw(txt)

    def poll(self):
        return Command(input("> "), repr(self), "root@shell")

    def input(self):
        while not self._stopped:
            e = self.poll()
            if not e.txt:
                continue
            dispatch(self, e)
            e.wait()

    def raw(self, txt):
        print(txt)

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        setcompleter(self.cmds)
        launch(self.input)
