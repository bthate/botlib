# OKLIB - the ok library !
#
# list of bots.

from .obj import Object, get_type
from .hdl import Loader

class Fleet(Object):

    bots = []

    def __iter__(self):
        return iter(Fleet.bots)

    def add(self, bot):
        Fleet.bots.append(bot)

    def announce(self, txt, skip=[]):
        for h in self.bots:
            if skip and type(h) in skip:
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        for b in Fleet.bots:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        for o in Fleet.bots:
            if repr(o) == orig:
                return o

    def by_cls(self, otype, default=None):
        res = []
        for o in Fleet.bots:
            if isinstance(o, otype):
                res.append(o)
        return res

    def by_type(self, otype):
        res = []
        for o in Fleet.bots:
            if otype.lower() in str(type(o)).lower():
                res.append(o)
        return res

    def say(self, orig, channel, txt):
        for o in Fleet.bots:
            if repr(o) == orig:
                o.say(channel, txt)
