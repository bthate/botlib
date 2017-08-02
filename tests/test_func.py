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

import os
import logging
import termios
import string
import random
import time
import types
import unittest

class Test_Func(unittest.TestCase):

    def test_func(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launcher.launch(functest, x)
            thr.join()

def randomarg(name):
    t = random.choice(types.__all__)
    return types.new_class(t)()
    
def functest(nr):
    names = sorted(kernel.modules("botlib"))
    for x in range(nr):
        random.shuffle(names)
        for name in names:
            mod = kernel.load(name)
            keys = dir(mod)
            random.shuffle(keys)
            for key in keys:
                obj = getattr(mod, key)
                if not obj:
                    for func in dir(obj):
                        if func and type(func) in [types.FunctionType, types.MethodType]:
                            arglist = []
                            for name in func.__code__.co_varnames:
                                 nrvar = func.__code__.co_argcount
                                 n = randomarg(name)
                                 if n:
                                     arglist.append(n)
                            try:
                                func(*arglist[:nrvar])
                            except:
                                logging.error(get_exception())
               
