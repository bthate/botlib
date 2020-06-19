# BOTLIB - the bot library !
#
#

import importlib, inspect, os, pkg_resources, queue

from .utl.gnr import get_type
from .utl.prs import Parsed
from .utl.trc import get_exception
from .obj import Default, Object
from .tbl import names

class NOTIMPLEMENTED(Exception):

    pass

class ETYPE(Exception):

    pass

class Event(Parsed):

    pass
        

class Handler(Object):
 
    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.queue = queue.Queue()
        self.names = names
                
    def dispatch(self, event):
        func = self.get_cmd(event.cmd)
        if func:
            func(event)
            event.show()

    def get_cmd(self, cmd, dft=None):
        name = self.names.get(cmd, dft)
        if name:
            mod = direct(name)
            return getattr(mod, cmd, None)

    def handler(self):
        while 1:
            e = self.queue.get()
            if e == None:
                break
            self.dispatch(e)

    def load_mod(self, name):
        mod = super().load_mod(name)
        self.cmds.update(find_cmds(mod))
        return mod

    def put(self, event):
        self.queue.put(event)

    def register(self, cmd, cb):
        self.cmds[cmd] = cb

    def scan(self, mod):
        self.cmds.update(find_cmds(mod))

    def start(self):
        from .thr import launch
        launch(self.handler)
            
    def stop(self):
        self.queue.put(None)

def direct(self, name):
    return importlib.import_module(name)
