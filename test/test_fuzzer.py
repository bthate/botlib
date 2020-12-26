# BOTLIB - test_fuzzer.py
#
# this file is placed in the public domain

"call all methods"

# imports

import os, sys ; sys.path.insert(0, os.getcwd())

import inspect
import types
import unittest
import bot.obj
import bot.cmd

from bot.obj import Object, get, get_name
from bot.hdl import Event, Handler, cmd
from bot.prs import parse_cli
from bot.utl import get_exception, mods

# defines

def cb(event):
    print("yoo")

exclude = ["poll", "handler", "input", "doconnect", "raw", "start"]

class FuzzHandler(Handler):

    "fuzzing handler"

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)

    def direct(self, txt):
        if verbose:
            print(txt)

values = Object()
values["addr"] = ("localhost", 6667)
values["callback"] = cb
values["channel"] = "#bot"
values["d"] = {}
values["e"] = Event()
values["event"] = Event({"txt": "thr", "error": "test"})
values["func"] = cb
values["handler"] = FuzzHandler()
values["hdl"] = FuzzHandler()
values["key"] = "txt"
values['mn'] = "bot.cmd"
values["mns"] = "irc,udp,rss"
values["mod"] = bot.cmd
values["name"] = "bot"
values["nick"] = "bot"
values["o"] = Object()
values["orig"] = repr(values["hdl"])
values["obj"] = Event()
values["origin"] = "test@shell"
values["path"] = bot.obj.wd
values["perm"] = "USER"
values["permission"] = "USER"
values["pkgnames"] = "bot"
values["rssobj"] = Object()
values["sleep"] = 60.0
values["server"] = "localhost"
values["text"] = "yoo"
values["txt"] = "yoo"
values["value"] = Object()

# classes
        
class Test_Fuzzer(unittest.TestCase):

    def test_fuzz(self):
        global exc
        m = mods("bot")
        for x in range(cfg.index or 1):
            for mod in m:
                fuzz(mod)
        exc = []

# functions

def get_values(vars):
    args = []
    for k in vars:    
       res = get(values, k, None)
       if res:
           args.append(res)
    return args

def handle_type(name, o, ex):
    if debug and verbose:
        print("%s(%s) -> %s" % (name, o, ex))

def fuzz(mod, *args, **kwargs):
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if "_" in name:
            continue
        try:
            oo = o()
        except TypeError as ex:
            handle_type(name, o, ex)
            continue
        for name, meth in inspect.getmembers(oo):
            if "_" in name or name in exclude:
                continue
            try:
                spec = inspect.getfullargspec(meth)
                if "self" in spec.args:
                    args = get_values(spec.args[1:])
                else:
                    args = get_values(spec.args)
            except TypeError as ex:
                handle_type(name, meth, ex)
                continue
            try:
                res = meth(*args, **kwargs)
                if debug:
                    print("%s(%s) -> %s" % (get_name(meth), ",".join([str(x) for x in args]), res))
            except Exception as ex:
                if debug:
                    print(get_exception())

# runtime

cfg = parse_cli()
debug = "d" in cfg.opts
exc = []
result = []
verbose = "v" in cfg.opts
