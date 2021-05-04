# This file is placed in the Public Domain.

import os
import queue
import sys
import time
import threading
import _thread

from bus import Bus
from cmn import spl
from evt import Command, Event
from nms import Names
from obj import Object, dorepr
from prs import parseargs
from run import kernel
from thr import launch
from trc import exception

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

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def error(self, event):
        pass

    @staticmethod
    def getcmd(cmd):
        k = kernel()
        return k.getcmd(cmd)

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

    def initialize(self):
        Bus.add(self)
        self.register("cmd", docmd)

    def put(self, e):
        self.queue.put_nowait(e)

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

    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt):
        self.prompt = False
        e = self.event(txt)
        docmd(self, e)
        e.wait()
        return e

    @staticmethod
    def getcmd(cmd):
        k = kernel()
        return k.getcmd(cmd)

    def event(self, txt):
        c = Command()
        c.txt = txt
        c.orig = dorepr(self)
        return c

    def handle(self, e):
        super().put(e)

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


def docmd(hdl, obj):
    obj.parse()
    f = hdl.getcmd(obj.cmd)
    if f:
        f(obj)
        obj.show()
    obj.ready()

def end(hdl, obj):
    raise ENOMORE("bye!")
