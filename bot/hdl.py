# This file is placed in the Public Domain.

__version__ = 120

import os
import queue
import sys
import time
import threading
import _thread

from bot.bus import Bus
from bot.evt import Command, Event
from bot.nms import Names
from bot.obj import Object, cfg, dorepr
from bot.prs import parseargs
from bot.utl.cmn import spl
from bot.utl.thr import launch
from bot.utl.trc import exception

cblock = _thread.allocate_lock()

class ENOMORE(Exception):

    pass

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.ready = threading.Event()
        self.speed = "normal"
        self.stopped = False

    def addbus(self):
        Bus.add(self)

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def cmd(self, txt):
        self.prompt = False
        e = self.event(txt)
        docmd(self, e)
        e.wait()
        return e

    def error(self, event):
        pass

    def handler(self):
        while not self.stopped:
            e = self.queue.get()
            try:
                self.callbacks(e)
            except ENOMORE:
                e.ready()
                break
            except Exception as ex:
                e.ready()
                ee = Event()
                ee.trace = exception()
                ee.exc = ex
                self.error(ee)

    def put(self, e):
        self.queue.put_nowait(e)

    @staticmethod
    def reg(mns):
        import bot
        for mn in spl(mns):
            mod = getattr(bot, mn)
            if mod and "reg" in dir(mod):
                mod.reg()

    def register(self, name, callback):
        self.cbs[name] = callback

    def restart(self):
        self.stop()
        time.sleep(5.0)
        self.start()

    def start(self):
        self.stopped = False
        launch(self.handler)
        return self

    def stop(self):
        self.stopped = True
        e = Event()
        e.type = "end"
        self.queue.put(e)
        self.ready.set()

    def wait(self):
        self.ready.wait()

class Client(Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.stopped = False
        self.running = False
        self.initialize()

    def add(self, name, cmd):
        Names.modules[name] = cmd.__module__

    def addbus(self):
        Bus.add(self)

    def announce(self, txt):
        self.raw(txt)

    def event(self, txt):
        c = Command()
        c.txt = txt
        c.orig = dorepr(self)
        return c

    def getcmd(self, cmd):
        mn = Names.getmodule(cmd)
        mod = sys.modules.get(mn, None)
        return getattr(mod, cmd, None)

    def handle(self, e):
        super().put(e)

    def initialize(self):
        self.addbus()
        self.register("cmd", docmd)

    def input(self):
        while not self.stopped:
            e = self.once()
            self.handle(e)

    def once(self):
        txt = self.poll()
        return self.event(txt)

    def poll(self):
        return self.iqueue.get()

    def raw(self, txt):
        pass

    def restart(self):
        self.stop()
        time.sleep(2.0)
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        if self.running:
            return
        self.running = True
        super().start()
        launch(self.input)

    def stop(self):
        self.running = False
        self.stopped = True
        super().stop()
        self.ready.set()

def init(mns):
    for mn in spl(mns):
        mod = sys.modules.get(mn, None)
        if mod and "init" in dir(mod):
            mod.init()

def docmd(hdl, obj):
    obj.parse()
    f = hdl.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    obj.ready()

def end(hdl, obj):
    raise ENOMORE("bye!")
