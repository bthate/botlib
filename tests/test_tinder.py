# tinder tests.

import bot
import lo
import logging
import os
import random
import sys
import time
import unittest

k = lo.get_kernel()
k.walk("bot")
k.walk("lo")
c = lo.csl.Console()
k.fleet.bots.append(c)
event = lo.hdl.Event()
event.parse()

param = lo.Object()
param.ed = ["bot.irc.Cfg", "bot.rss.Cfg", "bot.krn.Cfg", "bot.irc.Cfg server localhost", "bot.irc.Cfg channel \#dunkbots", "bot.krn.Cfg modules bot.udp"]
param.delete = ["reddit", ]
param.display = ["reddit title,summary,link",]
param.log = ["yo!", ""]
param.fleet = ["0", "1", ""]
param.find = ["log yo", "todo yo", "rss reddit"]
param.meet = ["test@shell", "bart"]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
param.todo = ["yo!", ""]

class Event(lo.hdl.Event):

    def show(self):
        if lo.cfg.verbose:
            for txt in self.result:
                print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(event.index or 1):
            thrs.append(lo.thr.launch(tests, k))
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
        if lo.cfg.verbose:
            print(e.txt)
        k.put(e)
        events.append(e)
    return events
