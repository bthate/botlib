# BOTLIB - the bot library !
#
#

import bot.obj, os

from .krn import get_kernel
from .obj import Db, Object
from .utl import cdir, list_files, get_type

class Log(Object):

    pass

class Todo(Object):

    pass

k = get_kernel()

def cfg(event):
    k.cfg.last()
    try:
        k.cfg.server, k.cfg.channel, k.cfg.nick = event.args
        k.save()
    except:
        event.reply(k.cfg)
        return
    event.reply("ok")

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

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

def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def log(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.cmd.Log", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    l = Log()
    l.txt = event.rest
    l.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.cmd.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def v(event):
    from .krn import __version__
    event.reply("BOTLIB %s" % __version__)
