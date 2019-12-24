# BOTLIB - Framework to program bots.
#
# 

import bl
import logging
import queue
import threading
import types

def __dir__():
    return ("Task", "Launcher")

class Thr(threading.Thread):

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def run(self):
        func, args = self._queue.get()
        try:
            self._result = func(*args)
        except Exception as ex:
            logging.error(bl.trc.get_exception())

    def join(self, timeout=None):
        super().join(timeout)
        return self._result


class Launcher:

    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False

    def launch(self, func, *args, **kwargs):
        #if bl.k.cfg.verbose:
        #    logging.error("launch %s %s (%s)" % (bl.utl.get_name(func), " ".join([str(x) for x in args]), bl.trc.get_from(2)))
        name = ""
        try:
            name = kwargs.get("name", args[0].name or args[0].txt)
        except (AttributeError, IndexError):
            name = bl.utl.get_name(func)
        t = Thr(func, *args, name=name)
        t.start()
        return t

    def start(self):
        while not self._stopped:
            t = self._queue.get()
            t.start()
