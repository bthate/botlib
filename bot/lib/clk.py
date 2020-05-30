# LIBOBJ - library to manipulate objects.
#
#

"""timers/repeaters."""

import bot.lib as lib
import threading
import time
import typing

def __dir__():
    return ("Repeater", "Timer", "Timers")

class Timer(lib.Object):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.sleep = sleep
        self.args = args
        self.name = kwargs.get("name", "")
        self.kwargs = kwargs
        self.state = lib.Object()
        self.timer = None

    def run(self, *args, **kwargs):
        self.state.latest = time.time()
        lib.thr.launch(self.func, *self.args, **self.kwargs)

    def start(self):
        if not self.name:
            self.name = lib.typ.get_name(self.func)
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self.name)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        thr = lib.thr.launch(self.start)
        self.func(*args, **kwargs)
        return thr
