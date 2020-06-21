# BOTLIB - the bot library !
#
#

import pkg_resources, queue, threading

from .itr import find_cmds, direct
from .obj import Object
from .prs import Parsed
from .thr import launch

class NOTIMPLEMENTED(Exception):

    pass

class ETYPE(Exception):

    pass

class Event(Parsed):

    def __init__(self):
        super().__init__()
        self.started = threading.Event()
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
        self.started.wait()
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
        self.speed  = "fast"
        self.stopped = False

    def cmd(self, txt):
        if not txt:
            return
        e = Event()
        e.parse(txt)
        e.orig = repr(self)
        self.dispatch(e)
        return e
                
    def dispatch(self, event):
        if not event.txt:
            return
        event.parse(event.txt)            
        if not event.cmd and event.txt:
            event.cmd = event.txt.split()[0]
        event.func = self.get_cmd(event.cmd)
        if event.func:
            event.func(event)
        event.show()
        event.started.set()
                    
    def get_cmd(self, cmd, dft=None):
        func = self.cmds.get(cmd, None)
        if not func:
            try:
                name = self.names.get(cmd, None)
            except:
                name = None
            if name:
                self.load_mod(name)
                func = self.cmds.get(cmd, dft)
        return func

    def handler(self):
        while not self.stopped:
            event = self.queue.get()
            if not event.orig:
                event.orig = repr(self)
            event.speed = self.speed
            thr = launch(self.dispatch, event, name=event.txt)
            event.thrs.append(thr)

    def load_mod(self, name):
        mod = direct(name)
        self.cmds.update(find_cmds(mod))
        return mod

    def scan(self, mod):
        print("scan %s" % mod.__name__)
        self.cmds.update(find_cmds(mod))

    def start(self):
        launch(self.handler)

    def walk(self, name):
        for fname in pkg_resources.resource_listdir(name, ""):
            if fname.startswith("_") or not fname.endswith(".py"):
                continue
            mod = direct("%s.%s" % (name, fname[:-3]))
            self.scan(mod)
