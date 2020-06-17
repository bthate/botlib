# BOTLIB - the bot library !
#
#

import importlib, inspect, os, pkg_resources, queue
import sys, threading, time, types, _thread

from .cbs import dispatch
from .obj import Cfg, Default, DoL, Object
from .thr import Launcher
from .utl import elapsed, fntime, get_exception, get_type

class Loader(Object):

    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.table = Object()

    def direct(self, name):
        return importlib.import_module(name)

    def find_all(self, pkgs="bot"):
        mns = Object()
        for p in pkgs.split(","):
            for mod in self.find_modules(p):
                mns.update(self.find_names(mod))
        return mns

    def find_callbacks(self, mod):
        cbs = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 2:
                cbs[key] = o
        return cbs

    def find_cmds(self, mod):
        cmds = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    cmds[key] = o
        return cmds

    def find_modules(self, pkgs, filter=None):
        mods = []
        for pkg in pkgs.split(","):
            if filter and filter not in mn:
                continue
            try:
                p = self.direct(pkg)
            except ModuleNotFoundError:
                continue
            for key, m in inspect.getmembers(p, inspect.ismodule):
                if m not in mods:
                    mods.append(m)
        return mods

    def find_names(self, mod):
        names = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    names[key] = o.__module__
        return names

    def find_shorts(self, mn):
        shorts = DoL()
        for mod in self.find_modules(mn):
            for key, o in inspect.getmembers(mod, inspect.isclass):
                if issubclass(o, Object) and key == o.__name__.lower():
                    t = "%s.%s" % (o.__module__, o.__name__)
                    shorts.append(o.__name__.lower(), str(t))
        return shorts

    def find_types(self, mn):
        res = []
        for mod in self.find_modules(mn):
            for key, o in inspect.getmembers(mod, inspect.isclass):
                if issubclass(o, Object):
                    t = "%s.%s" % (o.__module__, o.__name__)
                    res.append(t)
        return res

    def get_cmd(self, cmd):
        for mod in self.table:
            res = getattr(mod, cmd, None)
            if not res:
               continue
            return res

    def load_mod(self, mn):
        if mn in self.table:
            return self.table[mn]
        self.table[mn] = self.direct(mn)
        return self.table[mn]

    def walk(self, mns):
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            try:
                for x in pkg_resources.resource_listdir(mn, ""):
                    if x.startswith("_") or not x.endswith(".py"):
                        continue
                    module = self.direct("%s.%s" % (mn, x[:-3]))
                    mods.append(module)
            except ModuleNotFoundError:
                continue
            except TypeError:
                mod = self.direct(mn)
                try:
                    for pkg in mod.__path__:
                        for x in os.listdir(pkg):
                            if x.startswith("_") or not x.endswith(".py"):
                                continue
                            mmn = "%s.%s" % (mod.__name__, x[:-3])
                            module = self.direct(mmn)
                            mods.append(module)
                except AttributeError:
                    x = mod.__qualname___
                    if x.startswith("_") or not x.endswith(".py"):
                        continue
                    module = self.direct(x)
                    mods.append(module)
        return mods
        
    def wait(self, nrsec=0):
        while not self._stopped:
            time.sleep(0.1)

    def scan(self, pkgs="bot"):
        res = []
        for mod in self.walk(pkgs):
            cmds = self.find_cmds(mod)
            if cmds:
                self.load_mod(mod.__name__)
                res.append(mod)
                self.cmds.update(cmds)
        return res

class Handler(Loader, Launcher):
 
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self.cbs = Object()

    def handle_cb(self, event):
        if event.etype in self.cbs:
            self.cbs[event.etype](self, event)
        
    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            if e == None:
                break
            self.handle_cb(e)

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put(event)

    def ready(self):
        self._ready.set()

    def register(self, cbname, handler):
        self.cbs[cbname] = handler        

    def start(self, handler=True):
        if handler:
            self.launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

class Event(Default):

    def __init__(self, txt=""):
        super().__init__()
        self._ready = threading.Event()
        self._result = []
        self._thrs = []
        self.etype = "event"
        self.txt = txt
                
    def display(self, o, txt="", keys=None, options="t", post="", strict=False):
        if not keys:
            keys = list(o.keys())
        txt = txt[:]
        txt += " %s" % self.format(o, keys, strict=strict) 
        if "t" in options:
           txt += " %s" % elapsed(time.time() - fntime(o._path))
        if post:
           txt += " " + post
        txt = txt.strip()
        self.reply(txt)

    def format(self, o, keys=None, strict=False):
        if keys is None:
            keys = list(vars(o).keys())
        res = []
        txt = ""
        for key in keys:
            val = o.get(key)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append((key, val))
        for key, val in res:
            if strict:
                txt += "%s%s" % (val.strip(), " ")
            else:
                txt += "%s=%s%s" % (key, val.strip(), " ")
        return txt.strip()

    def parse(self):
        spl = self.txt.split()
        if spl:
            self.cmd = spl[0].lower()
            self.args = spl[1:]
            self.rest = " ".join(self.args)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)
 
    def show(self):
        for txt in self._result:
            print(txt)
            
    def wait(self, nrsec=30.0):
        self._ready.wait(nrsec)

class Command(Event):

    def __init__(self, txt=""):
        super().__init__(txt)
        self.etype = "command"
