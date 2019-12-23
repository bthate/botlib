# BOTLIB - Framework to program bots.
#
# 

import sys
import bl
import bl.evt
import bl.hdl

def __dir__():
    return ("Console",)

class Console(bl.hdl.Handler):

    def __init__(self):
        super().__init__()
        self.verbose = True
        
    def announce(self, txt: str) -> None:
        self.raw(txt)

    def poll(self) -> None:
        e = bl.evt.Event()
        e.options = bl.k.cfg.options
        e.orig = repr(self)
        e.origin = "root@shell"
        e.txt = input("> ")
        return e

    def input(self) -> None:
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            bl.k.put(e)
            e.wait()

    def raw(self, txt: str) -> None:
        if not self.verbose or not txt:
            return
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel: str, txt: str, type="chat") -> None:
        self.raw(txt)
 
    def start(self, handler=False, input=True, output=False) -> None:
        bl.k.add(self)
        super().start(handler, input, output)
