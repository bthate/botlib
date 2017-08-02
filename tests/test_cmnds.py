# BOTLIB - Framework to program bots.
#
# 

from botlib.event import Event
from botlib.error import ENODATE
from botlib.object import Object
from botlib.space import cfg, fleet, kernel, launcher, users
from botlib.options import opts_defs
from botlib.trace import get_exception
from botlib.utils import stripped, sname
from botlib.template import varnames, examples

import os
import logging
import termios
import string
import random
import time
import types
import unittest

class Test_Cmnds(unittest.TestCase):

    def test_run(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launcher.launch(testcmnds, event)
            thr.join()

    def test_func(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launcher.launch(functest, event)
            thr.join()

    def test_cmnd(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launcher.launch(cmndrun, event)
            thr.join()
        

def test():
    print("yooo!")

def randomarg():
    t = random.choice(types.__all__)
    return types.new_class(t)()
    
def cmndrun(event):
    for name in sorted(kernel.modules("botlib")):
        if name in ["botlib.test", "botlib.rss"]:
            continue
        mod = kernel.load(name)
        for n in dir(mod):
           if n in exclude:
               continue
           func = getattr(mod, n, None)
           if func and type(func) in [types.FunctionType, types.MethodType]:
               if "event" in func.__code__.co_varnames:
                   e = Event()
                   e._funcs.append(func)
                   e.origin = "root@shell"
                   e.server = "localhost"
                   e.btype = "cli"
                   kernel.put(e)

def functest(event):
    for name in sorted(kernel.modules("botlib")):
        if name in ["botlib.test", "botlib.rss"]:
            continue
        mod = kernel.load(name)
        keys = dir(mod)
        random.shuffle(keys)
        for n in keys:
           if n in exclude:
               continue
           obj = getattr(mod, n, None)
           for func in dir(obj):
               if  func and type(func) in [types.FunctionType, types.MethodType]:
                   arglist = []
                   for name in func.__code__.co_varnames:
                       nrvar = func.__code__.co_argcount
                       n = varnames.get(name, None)
                       if n:
                           arglist.append(n)
                   try:
                       func(*arglist[:nrvar])
                   except:
                       logging.error(get_exception())
               
def testcmnds(event):
    keys = list(kernel.list("botlib"))
    random.shuffle(keys)
    for cmnd in keys:
        if cmnd in exclude:
            continue
        if cmnd == "find":
            name = "email"
        else:
            name = randomarg()
        e = Event(event)
        e.btype = event.btype
        e.server = event.server
        cmnd = examples.get(cmnd, cmnd)
        e.txt = "%s %s" % (cmnd, name)
        e.origin = "root@shell"
        e.parse()
        kernel.put(e)

exclude = ["exit", "loglevel", "reboot", "real_reboot", "fetcher", "synchronize", "init", "shutdown", "wrongxml","mbox", "testcmnds", "runkernel", "functest", "cmndrun"]
outtxt = u"Đíť ìš éèñ ëņċøďıńğŧęŝţ· .. にほんごがはなせません .. ₀0⁰₁1¹₂2²₃3³₄4⁴₅5⁵₆6⁶₇7⁷₈8⁸₉9⁹ .. ▁▂▃▄▅▆▇▉▇▆▅▄▃▂▁ .. .. uǝʌoqǝʇsɹǝpuo pɐdı ǝɾ ʇpnoɥ ǝɾ"
