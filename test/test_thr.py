# This file is placed in the Public Domain.

import unittest

from bot import cfg
from bot.evt import Command
from bot.thr import launch

from test.prm import param
from test.run import h

events = []

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            launch(exec)
        consume(events)

def consume(elems):
    fixed = []
    res = []
    for e in elems:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    return res

def exec():
    for cmd in h.modnames:
        for ex in getattr(param, cmd, [""]):
            txt = cmd + " " + ex
            e = Command(txt)
            h.put(e)
            events.append(e)
