# tinder tests.

__version__ = 1

## imports

import logging, os, random, sys, time, unittest

from bot.spc import Object, Event, Command, get_kernel

## define

event = Event()
event.parse()

param = Object()
param.ed = ["bot.irc.Cfg", "bot.rss.Cfg", "bot.krn.Cfg", "bot.irc.Cfg server localhost", "bot.irc.Cfg channel \#dunkbots", "bot.krn.Cfg modules bot.udp"]
param.delete = ["reddit", ]
param.display = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.fleet = ["0", "1", ""]
param.find = ["log test2", "todo test3", "rss reddit"]
param.meet = ["test@shell", "bart"]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
param.todo = ["test4!", ""]

k = get_kernel()

## classes

class Event(Event):

    def show(self):
        for txt in self._result:
            print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        k = get_kernel()
        thrs = []
        for x in range(k.cfg.index or 1):
            thrs.append(k.launch(tests, k))
        for t in thrs:
            t.join()

    def test_all(self):
        k = get_kernel()
        for x in range(k.cfg.index or 1):
            tests(k)

## functions

def consume(elems):
    fixed = []
    for e in elems:
        print(e)
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
        exs = ["test1",]
    e = list(exs)
    random.shuffle(e)
    events = []
    for ex in e:
        txt = cmd + " " + ex
        e = Command(txt)
        k.dispatch(e)
        events.append(e)
    return events
