# tinder tests.

import logging
import os
import random
import sys
import time
import unittest

from lo import Object, cfg, get_kernel
from lo.csl import Console
from lo.hdl import Event
from lo.thr import launch

k = get_kernel()
k.walk("bot.mods")
c = Console()
k.fleet.bots.append(c)

event = Event()
event.parse()

param = Object()
param.ed = ["bot.irc.Cfg", "bot.rss.Cfg", "lo.krn.Cfg", "bot.irc.Cfg server localhost", "bot.irc.Cfg channel \#dunkbots", "lo.krn.Cfg modules bot.udp"]
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
        if cfg.verbose:
            for txt in self.result:
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
        e = Event()
        e.etype = "command"
        e.orig = repr(k)
        e.origin = "test@shell"
        e.txt = cmd + " " + ex
        if cfg.verbose:
            print(e.txt)
        k.put(e)
        events.append(e)
    return events
