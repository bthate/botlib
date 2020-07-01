# BOTLIB - the bot library !
#
#

import logging, os, random, sys, time, unittest

from bot.krn import k
from bot.hdl import Event
from bot.obj import Object
from bot.thr import launch

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

events = []
ignore = ["ps"]
nrtimes = 1

class Event(Event):

    def reply(self, txt):
        if "-v" in sys.argv:
            print(txt)

for x in sys.argv:
    try:
        nrtimes = int(x)
    except ValueError:
        continue

class Test_Tinder(unittest.TestCase):

    def test_all(self):
        for x in range(nrtimes):
            tests(k)

    def test_thrs(self):
        thrs = []
        for x in range(nrtimes):
            launch(tests, k)
        consume(events)
        
def consume(elems):
    fixed = []
    res = []
    for e in elems:
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    k.stop()
    return res
    
def tests(b):
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def do_cmd(cmd):
    exs = param.get(cmd, [""])
    e = list(exs)
    random.shuffle(e)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex + " (%s)" % nr
        if "-v" in sys.argv:
            print(txt)
        e = Event()
        e.txt = txt
        k.queue.put(e)
        events.append(e)
    return events
