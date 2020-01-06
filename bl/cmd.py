# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import time

from bl.dbs import Db
from bl.krn import kernels, __version__
from bl.tms import elapsed
from bl.usr import Users

# defines

def __dir__():
    return ("cmds", "meet", "u", "v")

# functions

def cmds(event):
    event.reply(",".join(k.cmds))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = Users.userhosts.get(origin, origin)
    u = k.users.meet(origin, perms)
    event.reply("added %s" % origin)

def u(event):
    res = ""
    db = Db()
    for o in db.all("bl.usr.User"):
        res += "%s," % o.user
    event.reply(res)

def v(event):
    event.reply("BOTD %s" % __version__)

# runtime

k = kernels.get("0", None)
# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import os
import time
import threading

from bl.obj import Object
from bl.dbs import Db

# defines

def __dir__():
    return ("Log", "Todo", "log", "todo")

# classes

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

# functions

def log(event):
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def todo(event):
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
