# This file is placed in the Public Domain.

import random
import unittest

from hdl import Bus
from nms import Names
from run import kernel

from prm import param

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        k = kernel()
        for x in range(k.cfg.index or 1):
            exec()
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
    return res

def exec():
    c = Bus.objs[0]
    l = list(Names.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            c.put(e)
            events.append(e)
