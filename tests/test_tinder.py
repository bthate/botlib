# tinder tests.

import logging, os, random, sys, time, unittest

from bot.krn import get_kernel
from bot.obj import Object
from bot.hdl import Command, Event
from bot.thr import launch

k = get_kernel()

event = Event()
event.parse()

param = Object()
param.ed = ["bot.irc.Cfg", "bot.rss.Cfg", "bot.krn.Cfg", "bot.irc.Cfg server localhost", "bot.irc.Cfg channel \#dunkbots", "bot.krn.Cfg modules bot.udp"]
param.delete = ["reddit", ]
param.display = ["reddit title,summary,link",]
param.log = ["yo!", ""]
param.fleet = ["0", "1", ""]
param.find = ["log yo", "todo yo", "rss reddit"]
param.meet = ["test@shell", "bart"]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
param.todo = ["yo!", ""]

class Event(Event):

    def show(self):
        for txt in self._result:
            print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(event.index or 1):
            thrs.append(launch(tests, k))
        for t in thrs:
            t.join()

    def test_all(self):
        for x in range(event.index or 1):
            tests(k)

def consume(elems):
    fixed = []
    for e in elems:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
        
def tests(b):
    events = []
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        events.extend(do_cmd(k, cmd))
    consume(events)
    k.ready()

def do_cmd(b, cmd):
    exs = param.get(cmd, [])
    if not exs:
        exs = ["bla",]
    e = list(exs)
    random.shuffle(e)
    events = []
    for ex in e:
        txt = cmd + " " + ex
        e = Command(txt, repr(k), "test@shell")
        print(txt)
        k.put(e)
        events.append(e)
    return events
