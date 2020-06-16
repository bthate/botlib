# BOTLIB - the bot library !
#
#

from .krn import get_kernel
from .irc import Cfg

def cfg(event):
    k = get_kernel()
    k.cfg.last()
    try:
        k.cfg.server, k.cfg.channel, k.cfg.nick = event.args
        k.save()
    except:
        event.reply(k.cfg)
        return
    event.reply("ok")
# BOTLIB - the bot library !
#
#

import bot.obj, os

from .dbs import Db
from .obj import ENOCLASS, get_cls
from .krn import get_kernel

k = get_kernel()

def list_files(wd):
    return "|".join([x for x in os.listdir(os.path.join(wd, "store"))])

def ed(event):
    if not event.args:
        event.reply(list_files(bot.obj.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = k.find_shorts("ok")
    if shorts:
        cn = shorts[0]
    db = Db()
    l = db.last(cn)
    if not l:
        try:
            c = get_cls(cn)
            l = c()
            event.reply("created %s" % cn)
        except ENOCLASS:
            event.reply(list_files(bot.obj.workdir) or "no files yet")
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        setter = {event.args[1]: ""}
    else:
        setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    l.save()
# BOTLIB - the bot library !.
#
#

import bot.obj, os, time

from .krn import get_kernel
from .obj import cdir
from .dbs import Db

def __dir__():
    return ("find",)

k = get_kernel()

def find(event):
    if not event.args:
        wd = os.path.join(bot.obj.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    db = Db()
    target = db.all
    otype = event.args[0]
    try:
       match = event.args[1]
       target = db.find_value
    except:
       match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for o in target(otype, match):
        nr += 1
        event.display(o, str(nr), args or o.keys())
    if nr == -1:
        event.reply("no %s found." % otype)
# BOTLIB - the bot library !
#
#

from .obj import get_type
from .krn import get_kernel

k = get_kernel()

def cmds(event):
    bot = k.fleet.by_orig(event.orig)
    if not bot:
        bot = k
    event.reply("|".join(sorted(bot.cmds)))

def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])
# BOTLIB - the bot library !
#
#

from .obj import Object
from .dbs import Db

def __dir__():
    return ("Todo", 'done', 'todo')

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def todo(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.tdo.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    got = []
    db = Db()
    for todo in db.find("bot.tdo.Todo", selector):
        todo._deleted = True
        todo.save()
        event.reply("ok")
        break
