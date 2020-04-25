# tinder tests.

import bot
import lo
import logging
import os
import random
import sys
import time
import unittest

k = bot.get_kernel()
e = lo.hdl.Event()
e.parse()

class Param(lo.Object):

    pass


param = Param()
param.cfg = ["irc", "rss", "krn", "irc server localhost", "irc channel \#dunkbots", "krn modules bot.udp"]
param.delete = ["reddit", ]
param.display = ["reddit title,summary,link",]
param.log = ["yo!", ""]
param.fleet = ["0", "1", ""]
param.find = ["log yo", "todo yo", "rss reddit"]
param.meet = ["test@shell", "bart"]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
param.todo = ["yo!", ""]

class Event(lo.hdl.Event):

    verbose = lo.cfg.verbose

    def show(self):
        if self.verbose:
            for txt in self.result:
                print(txt)

class Test_Tinder(unittest.TestCase):

    def test_tinder(self):
        thrs = []
        for x in range(e.index or 1):
            logging.debug("test %s" % x)
            thrs.append(lo.thr.launch(tests, k))
        for t in thrs:
            t.join()

    def test_tinder2(self):
        for x in range(e.index or 1):
            logging.debug("test %s" % x)
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
        e.options = lo.cfg.options
        e.verbose = lo.cfg.verbose
        print(e)
        k.put(e)
        events.append(e)
    return events
