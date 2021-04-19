# This file is in the Public Domain.

from .bus import Bus
from .obj import Object
from .prs import parseargs
from .zzz import threading

class Event(Object):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.done = threading.Event()
        self.exc = None
        self.result = []
        self.thrs = []
        self.type = "event"
        self.txt = None

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        if self.txt:
            parseargs(self, self.txt)

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def say(self, txt):
        Bus.say(self.orig, self.channel, txt.rstrip())

    def show(self):
        if self.exc:
            self.say(self.exc)
        for txt in self.result:
            self.say(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join(timeout)

class Command(Event):

    def __init__(self):
        super().__init__()
        self.type = "cmd"
