# BOTLIB - hdl.py
#
# this file is placed in the public domain

"handler (hdl)"

# imports

import inspect
import importlib
import importlib.util
import os
import queue
import threading
import time

from bot.dbs import list_files
from bot.obj import Default, Object, Ol, get, update
from bot.prs import parse
from bot.thr import launch
from bot.utl import direct, spl

# defines

__version__ = 116

def __dir__():
    return ("Bus", "Command", "Event", "Handler", "cmd")

# classes

class Bus(Object):

    "bus class - registered recipient event handler"

    objs = []

    def __call__(self, *args, **kwargs):
        return self.objs

    def __iter__(self):
        return iter(Bus.objs)

    def add(self, obj):
        "add listener to bus"
        Bus.objs.append(obj)

    def announce(self, txt, skip=None):
        "announce to all listeners"
        for h in self.objs:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def by_orig(self, orig):
        "fetch listener by orig"
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    def dispatch(self, event):
        for o in Bus.objs:
            o.dispatch(event)

    def say(self, orig, channel, txt):
        "say something to specific listener"
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))


class Event(Default):

    "event class"

    __slots__ = ("prs", "src")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.channel = ""
        self.done = threading.Event()
        self.orig = None
        self.result = []
        self.thrs = []
        self.type = "event"

    def direct(self, txt):
        "send txt to console - overload this"
        Bus.say(self.orig, self.channel, txt)

    def parse(self):
        "parse an event"
        self.prs = Default()
        parse(self.prs, self.otxt or self.txt)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = list(args)
            self.rest = " ".join(self.args)
            self.otype = args.pop(0)
        if args:
            self.xargs = args

    def ready(self):
        "event is handled"
        self.done.set()

    def reply(self, txt):
        "add txt to result"
        self.result.append(txt)

    def show(self, target=None):
        "display result"
        for txt in self.result:
            if target:
                target.say(self.channel, txt)
                continue
            self.direct(txt)

    def wait(self):
        "wait for event to be handled"
        self.done.wait()
        for thr in self.thrs:
            thr.join()

class Command(Event):

    def __init__(self, txt, **kwargs):
        super().__init__([], **kwargs)
        self.type = "cmd"
        if txt:
            self.txt = txt

class Handler(Object):

    "basic event handler"

    threaded = False

    def __init__(self):
        super().__init__()
        self.bus = Bus()
        self.cbs = Object()
        self.cmds = Object()
        self.names = Ol()
        self.queue = queue.Queue()
        self.stopped = False
        self.bus.add(self)

    def clone(self, hdl):
        "copy callbacks"
        update(self.cmds, hdl.cmds)
        update(self.cbs, hdl.cbs)
        update(self.names, hdl.names)

    def cmd(self, txt):
        "execute command"
        self.register("cmd", cmd)
        c = Command(txt)
        c.orig = repr(self)
        self.dispatch(c)
        c.wait()

    def direct(self, txt):
        "outputs text, overload this"

    def dispatch(self, event):
        "run callbacks for event"
        if event.type and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def files(self):
        "show files in workdir"
        import bot.obj
        assert bot.obj.wd
        return list_files(bot.obj.wd)

    def fromdir(self, path, name="bot"):
        "scan a modules directory"
        if not path:
            return
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            self.intro(direct("%s.%s" % (name, mn)))

    def init(self, mns, name="bot"):
        "call init() of modules"
        thrs = []
        for mn in spl(mns):
            try:
                spec = importlib.util.find_spec("%s.%s" % (name, mn))
            except ModuleNotFoundError:
                continue
            if spec:
                mod = self.intro(direct("%s.%s" % (name, mn)))
                func = getattr(mod, "init", None)
                if func:
                    thrs.append(func(self))
        return thrs

    def intro(self, mod):
        "introspect a module"
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if "obj" in o.__code__.co_varnames:
                    self.register(key, o)
                elif "event" in o.__code__.co_varnames:
                    self.cmds[key] = o
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)
        return mod

    def handler(self):
        "handler loop"
        self.running = True
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            e.thrs.append(launch(self.dispatch, e))

    def put(self, e):
        "put event on queue"
        self.queue.put_nowait(e)

    def register(self, name, callback):
        "register a callback"
        self.cbs[name] = callback

    def say(self, channel, txt):
        "forward to direct"
        self.direct(txt)

    def start(self):
        "start handler"
        launch(self.handler)

    def stop(self):
        "stop handler"
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames, name=""):
        "walk over packages and load their modules"
        if not name:
            name = list(spl(pkgnames))[0]
        for pn in spl(pkgnames):
            mod = direct(pn)
            self.fromdir(mod.__path__[0], name)

    def wait(self):
        "wait for handler stopped status"
        if not self.stopped:
            while 1:
                time.sleep(30.0)

# functions

def cmd(handler, obj):
    "callbackx to dispatch to command"
    obj.parse()
    f = get(handler.cmds, obj.cmd, None)
    if f:
        f(obj)
        obj.show(handler)
    obj.ready()

# runtime

debug = False
md = ""
