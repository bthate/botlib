# BOTLIB - the bot library !
#
#

__version__ = 1

## imports

import os, pkg_resources, queue

from .its import find_cmds
from .obj import Default, Object
from .utl import direct, get_exception, get_type

import bot.tbl

## classes

class NOTIMPLEMENTED(Exception):

    pass

class Loader(Object):

    def __init__(self):
        super().__init__()
        self.table = Object()

    def load_mod(self, name):
        self.table[name] = direct(name)
        return self.table[name]

class Handler(Loader):
 
    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.cmds = Object()
        self.queue = queue.Queue()

    def dispatch(self, event):
        if not event.txt:
            return
        cmd = event.txt.split()[0]
        func = self.get_cmd(cmd)
        if func:
            try:
                func(event)
            except Exception as ex:
                print(get_exception())
            event.show(self)

    def callback(self, event):
        t = get_type(event)
        if t in self.cbs:
            self.cbs[t](self, event)

    def get_cmd(self, cmd):
        name = bot.tbl.names.get(cmd, None)
        mod = None
        if name:
            mod = self.table.get(name)
        if not mod:
            print("autoload %s" % name)
            mod = self.load_mod(name)
        if mod:
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

    def scan(self, mod):
        from .its import find_cmds
        self.cmds.update(find_cmds(mod))

    def start(self):
        from .thr import launch
        launch(self.handler)
            
    def stop(self):
        self.queue.put(None)

class Event(Default):

    def __init__(self, txt=""):
        super().__init__()
        self.result = []
        self.txt = txt
        if self.txt:
            self.args = self.txt.split()[1:]
        else:
            self.args = []
        self.type = "event"

    def reply(self, txt):
        self.result.append(txt)
 
    def show(self, bot):
        for txt in self.result:
            bot.say(self.channel, txt)
