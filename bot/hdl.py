# BOTLIB - the bot library !
#
#

import importlib
import importlib.util
import importlib.resources
import os
import queue
import threading

from .isp import find_cmds, direct
from .obj import Default, Object
from .prs import parse
from .thr import launch

class NOTIMPLEMENTED(Exception):

    pass

class ETYPE(Exception):

    pass

class Event(Default):

    def __init__(self):
        super().__init__()
        self.result = []
        self.thrs = []

    def reply(self, txt):
        if not self.result:
            self.result = []
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            print(txt)

    def wait(self):
        res = []
        for thr in self.thrs:
            res.append(thr.join())
        return res

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.names = Object()
        self.queue = queue.Queue()
        self.speed = "fast"
        self.stopped = False

    def cmd(self, txt, event=None):
        e = Event()
        if event:
            e.update(event)
        e.txt = txt
        self.dispatch(e)
        return e

    def dispatch(self, e):
        p = parse(e, e.txt)
        func = self.get_cmd(p.cmd)
        if func:
            func(p)
        p.show()

    def find_mod(self, name):
        spec = importlib.util.find_spec(name)
        if not spec:
            return
        return importlib.util.module_from_spec(spec)

    def get_cmd(self, cmd, dft=None):
        func = self.cmds.get(cmd, None)
        if not func:
            name = self.names.get(cmd, None)
            if name:
                self.load_mod(name)
                func = self.cmds.get(cmd, dft)
        return func

    def handler(self):
        while not self.stopped:
            event = self.queue.get()
            if not event:
                break
            if not event.orig:
                event.orig = repr(self)
            event.speed = self.speed
            thr = launch(self.dispatch, event, name=event.txt)
            event.thrs.append(thr)

    def load_mod(self, name):
        mod = direct(name)
        self.scan(mod)
        return mod

    def scan(self, mod):
        self.cmds.update(find_cmds(mod))

    def start(self):
        launch(self.handler)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def walk(self, name):
        spec = importlib.util.find_spec(name)
        if not spec:
            return
        pkg = importlib.util.module_from_spec(spec)
        mods = []
        for pn in pkg.__path__:
            for fn in os.listdir(pn):
                if fn.startswith("_") or not fn.endswith(".py"):
                    continue
                mn = "%s.%s" % (name, fn[:-3])
                module = self.load_mod(mn)
                mods.append(module)
        return mods

