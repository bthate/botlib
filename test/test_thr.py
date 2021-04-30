# This file is placed in the Public Domain.

import random
import sys
import unittest

sys.path.insert(0, "test")

from bus import first
from evt import Command
from hdl import Client
from nms import Names
from obj import cfg, opts
from thr import launch

from prm import param

class Test(Client):

    def raw(self, txt):
        if opts("v"):
            print(txt)

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()

events = []

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    for e in events:
        print(e)
    return res

def exec():
    c = first()
    l = sorted(Names.modules)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            c.put(e)
            events.append(e)
