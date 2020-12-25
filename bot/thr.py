# BOTLIB - thr.py
#
# this file is placed in the public domain

"tasks (tsk)"

import os
import queue
import sys
import threading

from bot.obj import Default, Object
from bot.ofn import get_name

class Thr(threading.Thread):

    "task class"

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = 0
        self.state = Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        "run a task"
        func, args = self._queue.get()
        target = None
        if args:
            target = Default(vars(args[0]))
        self.setName((target and target.txt and target.txt.split()[0]) or self._name)
        self._result = func(*args)

    def wait(self, timeout=None):
        "wait for task to finish"
        super().join(timeout)
        return self._result
