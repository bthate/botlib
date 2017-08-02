# test_kernel.py
#
#

""" test for all command. """

from botlib.event import Event
from botlib.object import Object
from botlib.raw import RAW
from botlib.space import db, kernel, launcher, template
from botlib.options import opts_defs
from botlib.compose import compose

import readline
import unittest
import logging
import random
import string
import time
import types
import os

def test(event):
    event.reply("yo!")

classes = ["Bot", "IRC", "XMPP", "CLI", "Event", "Handler", "Task", "Object", "Default", "Config", "Launcher"]

#ignore = ["parse_cli", "builtin", "os", "sys", "log", "runkernel", "functest", "hello", "getline", "cmndrun", "fetcher", "testcmnds", "test", "runkernel", "reboot", "real_reboot", "shutdown", "loglevel", "testline", "connect"]
ignore = ["shutdown"]

examples = Object()
examples.find = "find todo"
examples.last = "last cfg"
examples.tommorrow = "tomorrow take some time off."
examples.deleted = "deleted rss"
examples.log = "log wakker"
examples.rss = "http://nos.nl"
examples.todo = "todo code some code"
examples.user = "user root@shell"
examples.timer = "timer 23.35 blablabla"
examples.show = "show fleet"
examples.shop = "shop bacon"
examples.rm = "rm rss[0]"
examples.restore = "restore rss[0]"
examples.reload = "reload cmnds"
examples.perm = "perm root@shell oper"
examples.meet = "meet root@shell oper"
examples.mbox = "mbox ~/25-1-2013"
examples.loglevel = "loglevel info"
examples.first = "first cfg"
examples.dump = "dump todo"
examples.delperm = "delperm root@shell oper"
examples.cfg = "cfg irc"
examples.announce = "announce bla"
examples.alias = "alias l cmnds"

varnames = Object()
varnames.object = Object(txt="test", date="Sat Jan 14 00:02:29 2017")
varnames.daystring = "2017-08-29 16:34:23.837288"
varnames.event = Event(txt="test")
varnames.seconds = 60
varnames.daystr = "Sat Jan 14 00:02:29 2017"
varnames.txt = "i told you so !!"
varnames.path = "data/runtime/kernel"
varnames.optionlist = "-b -a -l info"
varnames.level = "info"
varnames.error = "userdefined error message"
varnames.fd = 1
#varnames.old = termios.tcgetattr(1)
varnames.text = "blablabla mekker"
varnames.signature = "1e7f50d2015ac2ddc1f2ae8cf8ed6dfd896cab71"
varnames.options = opts_defs
varnames.u = "bart!~bart@localhost"
varnames.jid = "monitor@localhost/blamekker"
varnames.url = "http://localhost"
varnames.obj = {"bla": "mekker"}
varnames.func = test
varnames.timestamp = time.time()
varnames.origin = "root@shell"
varnames.perm = "OPER"
varnames.o = Object(txt="test")
varnames.depth = 2
varnames.keys = ["test", "txt"]
varnames.uniqs = ["bla"]
varnames.ignore = {"test": "mekker"}
varnames.notwant = {"test": "mekker"}
varnames.want = {"test": "mekker"}

def get_name(name):
    return varnames.get(name, "")

def randomarg(name):
    t = random.choice(classes)
    o = compose(t)
    return o()

bot = RAW()
bot.start()

class Test_Kernel(unittest.TestCase):

    def test_kernel(self):
        from botlib.space import kernel
        events = []
        bid = bot.id()
        cmnds = list(examples.keys())
        for x in range(1, 50):
            random.shuffle(cmnds)
            for cmnd in cmnds:
                if cmnd in ignore:
                    continue
                e = Event()
                e.bid = bid
                e.origin = "root@shell"
                e.txt = cmnd + " " + get_name(cmnd)
                kernel.put(e)
                events.append(e)
        for event in events:
            event.wait()
