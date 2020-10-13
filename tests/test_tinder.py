# BOTLIB - the bot library !
#
#

import ol
import os
import random
import sys
import time
import unittest

param = ol.Object()
param.add = ["test@shell", "bart"]
param.dne = ["test4", ""]
param.edt = ["mymod.rss.Cfg", "mymod.rss.Cfg server=localhost", "mymod.rss.Cfg channel=#dunkbots"]
param.rm = ["reddit", ]
param.dpl = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg server==localhost", "kernel mods==rss", "rss rss==reddit", "email From==pvp"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.mbx = ["~/Desktop/25-1-2013", ""]

events = []
ignore = ["mbx",]
nrtimes = 1

k = ol.krn.get_kernel()

class Event(ol.evt.Event):

    def reply(self, txt):
        if "v" in k.cfg.opts:
            print(txt)

class Test_Tinder(unittest.TestCase):


    def test_thrs(self):
        thrs = []
        for x in range(k.cfg.index or 1):
            ol.tsk.launch(tests, k)
        consume(events)

    def test_neuman(self):
        for e in do_cmd("mbx"):
            e.wait()
        for x in range(k.cfg.index or 1):
            tests(k)
        
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
    exs = ol.get(param, cmd, [""])
    e = list(exs)
    random.shuffle(e)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex 
        e = Event()
        e.txt = txt
        k.queue.put(e)
        events.append(e)
    return events
