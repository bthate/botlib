# BOTLIB - the bot library !
#
#

__version__ = 1

import bot.tbl, os, time

from .fil import cdir
from .obj import ENOCLASS, Cfg, Db, Object, format, get_cls, get_type, last, load, save
from .krn import k
from .tms import elapsed, fntime

class Log(Object):

    pass

class Todo(Object):

    pass

def cfg(event):
    from .irc import Cfg
    c = Cfg()
    last(c)
    if len(event.args) == 3:
        c.server, c.channel, c.nick = event.args
    elif len(event.args) == 2:
        c.server, c.channel = event.args
    elif len(event.args) == 1:
        c.server = event.args[0]
    save(c)
    event.reply(format(c))
        
def cmds(event):
    event.reply("|".join(sorted(bot.tbl.cmds)))

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    got = []
    db = Db()
    for todo in db.find("bot.cmd.Todo", selector):
        todo._deleted = True
        save(todo)
        event.reply("ok")
        break

def ed(event):
    if not event.args:
        event.reply(list_files(k.cfg.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = k.find_shorts("bot")
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
    edit(l, setter)
    save(l)
    event.reply("ok")

def find(event):
    import bot.obj
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
        res = db.find("bot.cmd.Log", {"txt": ""})
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("log what ?")
        return
    l = Log()
    l.txt = event.rest
    p = save(l)
    event.reply("ok %s" % p)

def todo(event):
    db = Db()
    if not event.rest:
        res = db.find("bot.cmd.Todo", {"txt": ""})
        if not res:
            return
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("do what ?")
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")

def v(event):
    from bot.krn import __version__
    event.reply("%s %s" % (k.cfg.name.upper() or "BOTLIB", k.cfg.version or __version__))

