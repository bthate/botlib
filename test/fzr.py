# This file is placed in the Public Domain.

import inspect
import ob
import ob.hdl
import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from ob import Object, cfg, get, get_name, mods, op
from ob.csl import Test
from ob.evt import Event
from ob.hdl import Handler, cb_cmd
from ob.utl import get_exception

from test.run import h, debug

def cb():
    if debug and op("v"):
        print("yoo")

exclude = ["poll", "handler", "input", "doconnect", "raw", "start"]
exc = []
result = []

values = Object()
values["daemonic"] = True
values['url'] = "http://rtfd.io"
values['code'] = 200
values['msg'] = "OK"
values['hdrs'] = {}
values['fp'] = "bla"
values["addr"] = ("127.0.0.1", 6667)
values["reason"] = "whyyyyy????"
values["channel"] = "#ob"
values["mn"] = "prs"
values["cmd"] = "PRIVMSG"
values["txt"] = "yoo2"
values["key"] = "txt"
values["value"] = Object()
values["d"] = {}
values["hdl"] = Handler()
values["event"] = Event(**{"txt": "thr", "orig": repr(h), "error": "test"})
values["pevent"] = Event(**{"txt": "thr", "orig": repr(h), "error": "test"})
values["dccevent"] = Event(**{"txt": "thr", "orig": repr(h), "error": "test"})
values["path"] = cfg.wd
values["channel"] = "#ob"
values["orig"] = repr(values["hdl"])
values["obj"] = h
values["rssobj"] = Object({"rss": "https://www.reddit.com/r/python/.rss"})
values["value"] = 1
values["pkgnames"] = "ob"
values["name"] = "ob"
values["callback"] = cb
values["e"] = Event({"txt": "thr", "orig": repr(h), "error": "test"})
values["mod"] = cb_cmd
values["mns"] = "irc,udp,rss"
values["sleep"] = 60.0
values["func"] = cb
values["origin"] = "test@shell"
values["perm"] = "USER"
values["permission"] = "USER"
values["text"] = "yoo"
values["server"] = "localhost"
values["nick"] = "bot"
values["o"] = Object()
values["handler"] = Handler()
values["skip"] = []

class Test_Fuzzer(unittest.TestCase):

    def test_fuzz(self):
        global exc
        m = mods("ob")
        for x in range(cfg.index or 1):
            for mod in m:
                fuzz(mod)
        exc = []

def get_values(vars):
    args = []
    for k in vars:
        res = get(values, k, None)
        if res is not None:
            args.append(res)
    return args

def fuzz(mod, *args, **kwargs):
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if not issubclass(o, Object):
            continue
        if "_" in name:
            continue
        try:
            sig = inspect.signature(o.__init__)
            arg = sig.parameters.keys()
            args = get_values(arg)
            oo = o(*args, **kwargs)
        except TypeError as ex:
            continue
        oo.stopped = True
        for name, meth in inspect.getmembers(oo, inspect.ismethod):
            if "_" in name or name in exclude:
                continue
            try:
                sig = inspect.signature(meth)
                arg = sig.parameters.keys()
                args = get_values(arg)
                res = meth(*args, **kwargs)
            except RuntimeError:
                pass
            except ob.irc.ENOUSER:
                continue
            except Exception as ex:
                exc.append((get_name(meth), get_exception()))
    if exc and op("v"):
        for e in exc:
            print(e) 
