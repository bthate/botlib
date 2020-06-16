# BOTLIB - the bot library !
#
#

import sys, threading

from .krn import get_kernel
from .hdl import Command, Loader
from .shl import setcompleter

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
            k.dispatch(e)
            e.wait()

    def raw(self, txt):
        print(txt)

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        setcompleter(self.cmds)
        k.launch(self.input)
