# BOTLIB - the bot library !
#
#

__version__ = 87

import inspect, os, sys, threading, time, traceback, _thread

from .prs import Parsed
from .tms import elapsed
from .trc import get_exception
from .obj import Cfg, Db, Object, get_type
from .hdl import Handler

starttime = time.time()

class ENOKERNEL(Exception):

    pass

class ENOUSER(Exception):

    pass


class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)
        
    def cmd(self, txt):
        if not txt:
            return
        e = Event()
        e.parse(txt)
        e.orig = repr(self)
        self.dispatch(e)
        return e

    def dispatch(self, event):
        if not event.cmd and event.txt:
            event.cmd = event.txt.split()[0]
        event.func = self.get_cmd(event.cmd)
        if event.func:
            event.func(event)
        event.show()

    def say(self, channel, txt):
        print(txt)

    def start(self, cfg={}):
        super().start()
        self.cfg.update(cfg)

    def stop(self):
        self.queue.put(None)

    def wait(self):
        while 1:
            time.sleep(1.0)

class Cfg(Cfg):

    pass

class Event(Parsed):

    def __init__(self):
        super().__init__()
        self.result = []
        self.thrs = []

    def reply(self, txt):
        if not self.result:
            self.result = []
        self.result.append(txt)
        
    def show(self):
        for txt in self.result:
            k.fleet.say(self.orig, self.channel, txt)

    def wait(self):
        for thr in self.thrs:
            thr.join()

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
                o.say(channel, str(txt))

class User(Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Db):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = self.userhosts.get(origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return self.all("bot.usr.User", s)

    def get_user(self, origin):
        u =  list(self.get_users(origin))
        if u:
            return u[-1]
 
    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

k = Kernel()

def get_kernel():
    return k

