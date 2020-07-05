# BOTLIB - the bot library !
#
#

import random, sys, time, unittest

from bot.krn import k
from bot.hdl import Event
from bot.obj import Object, get
from bot.thr import launch

events = []
ignore = ["ps"]

class Event(Event):

    def reply(self, txt):
        if "-v" in sys.argv:
            print(txt)

class Test_Threads(unittest.TestCase):

    def test_thrs(self):
        for x in range(k.cfg.index or 1):
            launch(tests, k)
        consume(events)
        
def consume(elems):
    fixed = []
    res = []
    for e in elems:
        print(e)
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    return res
    
def tests(b):
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        e = Event()
        e.txt = cmd + " " + "bla"
        k.queue.put(e)
        events.append(e)
        