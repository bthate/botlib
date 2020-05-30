# LIBOBJ - library to manipulate objects.
#
#

"""console."""

import bot.lib as lib
import bot.lib.exp as exp
import bot.lib.hdl as hdl
import bot.lib.thr as thr

import sys
import threading

def init(kernel):
    c = Console()
    c.start()
    c.wait()
    return c

class Console(hdl.Handler):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._ready = threading.Event()
        self._threaded = False
        
    def announce(self, txt):
        self.raw(txt)

    def poll(self):
        self._connected.wait()
        e = hdl.Event()
        e.etype = "command"
        e.origin = "root@shell"
        e.orig = repr(self)
        e.txt = input("> ")
        if not e.txt:
            raise lib.exp.ENOTXT 
        return e

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except lib.exp.ENOTXT:
                continue
            except EOFError:
                break
            lib.hdl.dispatch(self, e)
            e.wait()
        self._ready.set()

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self, handler=False, input=True):
        if self.error:
            return
        super().start(handler)
        if input:
            thr.launch(self.input)
        self._connected.set()

    def wait(self):
        if self.error:
            return
        self._ready.wait()
