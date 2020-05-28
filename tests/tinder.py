# MYBOT - IRC bot you can program your own commands for.
#
# tinder test

import bot
import lo
import logging
import os
import random
import sys
import time
import unittest

from lo.csl import Console
from lo.hdl import Command
from lo.thr import launch

e = Event()

param = lo.Object()
param.cfg = ["irc", "rss", "krn", "irc server localhost", "irc channel \#dunkbots", "krn modules bot.udp"]
param.delete = ["reddit", ]
param.display = ["reddit title,summary,link",]
param.log = ["yo!", ""]
param.fleet = ["0", "1", ""]
param.find = ["log yo", "todo yo", "rss reddit"]
param.meet = ["test@shell", "bart"]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
param.todo = ["yo!", ""]

k = lo.get_kernel()
events = []
ignore = ["tinder",]
lo.cfg.debug = True

def tinder(event):
    oldwd = lo.workdir
    lo.workdir = "testdata"
    global events
    events = []
    k = lo.get_kernel()
    if lo.cfg.txt:
        k.start()
    for x in range(event.index):
        tests(k)
    consume(events)
    lo.workdir = oldwd

def tests(b):
    k = lo.get_kernel()
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        do_cmd(k, cmd)

def do_cmd(b, cmd):
    if cmd in ignore:
        return []
    k = lo.get_kernel()
    exs = param.get(cmd, [])
    if not exs:
        exs = ["bla",]
    exx = list(exs)
    random.shuffle(exx)
    for ex in exx:
        txt = cmd + " "+ ex
        c = Command(txt, "test@shell", repr(k))
        c.verbose = lo.cfg.verbose
        c.parse()
        k.put(c)
        events.append(c)

def consume(elems):
    fixed = []
    for e in elems:
        logging.debug("wait %s" % e.txt)
        e.wait(1.0)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
