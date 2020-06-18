# BOTLIB - the bot library !
#
#

import importlib, inspect, os, pkg_resources, queue

from .obj import Default, Object
from .utl import get_exception, direct, get_type

class NOTIMPLEMENTED(Exception):

    pass

class ETYPE(Exception):

    pass

class Loader(Object):

    def __init__(self):
        super().__init__()
        self.table = Object()

    def load_mod(self, name):
        if not name:
            return
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

    def get_cmd(self, cmd, dft=None):
        import bot.tbl
        name = bot.tbl.names.get(cmd, dft)
        mod = None
        if name:
            mod = self.table.get(name)
        if not mod:
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
        self.cmds.update(find_cmds(mod))

    def start(self):
        from .thr import launch
        launch(self.handler)
            
    def stop(self):
        self.queue.put(None)

class Event(Default):

    def __init__(self, txt=""):
        super().__init__()
        if type(txt) != str:
            raise ETYPE(str(type(txt)))
        self.type = "event"
        self.result = []
        self.txt = txt
        if self.txt:
            self.args = self.txt.split()[1:]
        else:
            self.args = []
        self.rest = " ".join(self.args)

    def reply(self, txt):
        self.result.append(txt)
 
    def show(self, bot):
        for txt in self.result:
            bot.say(self.channel, txt)

## inspectors

def find_names(mod):
    names = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                names[key] = o.__module__
    return names

def find_allnames(name):
    mns = Object()
    pkg = direct(name)
    for mod in find_modules(pkg):
        mns.update(find_names(mod))
    return mns

def find_callbacks(mod):
    cbs = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
       if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 2:
                cbs[key] = o
    return cbs

def find_cmds(mod):
    cmds = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
       if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                cmds[key] = o
    return cmds

def find_modules(pkgs, filter=None):
    mods = []
    for pkg in pkgs.split(","):
        if filter and filter not in mn:
            continue
        try:
            p = direct(pkg)
        except ModuleNotFoundError:
            continue
        for key, m in inspect.getmembers(p, inspect.ismodule):
            if m not in mods:
                mods.append(m)
    return mods


def find_shorts(mn):
    shorts = {}
    for mod in find_modules(mn):
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object) and key == o.__name__.lower():
                t = "%s.%s" % (o.__module__, o.__name__)
                shorts[o.__name__.lower()] = t.lower()
    return shorts

def find_types(mn):
    res = []
    for mod in find_modules(mn):
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                res.append(t)
    return res

def resources(name):
    resources = {}
    for x in pkg_resources.resource_listdir(name, ""):
        if x.startswith("_") or not x.endswith(".py"):
            continue
        mmn = "%s.%s" % (mn, x[:-3])
        resources[mmn] = direct(mmn)
    return mmn

def walk(name):
    mods = {}
    mod = direct(name)
    for pkg in mod.__path__:
        for x in os.listdir(pkg):
            if x.startswith("_") or not x.endswith(".py"):
                continue
            mmn = "%s.%s" % (mod.__name__, x[:-3])
            mods[mmn] = direct(mmn)
    return mods
