# OLIB - object library
#
#

import importlib
import ol
import pkgutil
import queue
import threading
import _thread

dispatchlock = _thread.allocate_lock()

class Event(ol.Object):

    def __init__(self):
        super().__init__()
        self.args = []
        self.cmd = ""
        self.prs = ol.Object()
        self.ready = threading.Event()
        self.rest = ""
        self.result = []
        self.thrs = []
        self.txt = ""

    def direct(self, txt):
        ol.bus.bus.say(self.orig, self.channel, txt)

    def parse(self):
        o = ol.Default()
        ol.prs.parse(o, self.txt)
        ol.update(self.prs, o)
        args = self.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = args
            self.rest = " ".join(args)
            
    def reply(self, txt):
        if not self.result:
            self.result = []
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            try:
                print(txt)
            except:
               pass

    def wait(self):
        self.ready.wait()
        res = []
        for thr in self.thrs:
            res.append(thr.join())
        return res

class Handler(ol.ldr.Loader):

    def __init__(self):
        super().__init__()
        self.packages = []
        self.queue = queue.Queue()
        self.stopped = False

    def dispatch(self, e):
        e.parse()
        if e.cmd not in self.cmds:
            mn = ol.get(ol.tbl.mods, e.cmd, None)
            if mn:
                self.load(mn)
        if e.cmd in self.cmds:
            try:
                self.cmds[e.cmd](e)
                e.show()
                e.ready.set()
            except Exception as ex:
                print(ol.utl.get_exception())
        e.ready.set()

    def handler(self):
        while not self.stopped:
            event = self.queue.get()
            if not event:
                break
            if "orig" not in event:
                event.orig = repr(self)
            if event.txt:
                if self.cfg.nothread:
                    self.dispatch(event)
                else:
                    ol.tsk.launch(self.dispatch, event)
            else:
                event.ready.set()

    def put(self, e):
        self.queue.put_nowait(e)

    def start(self):
        ol.tsk.launch(self.handler)

    def stop(self):
        self.stopped = True
        self.queue.put(None)
