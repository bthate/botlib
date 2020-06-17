# BOTLIB - the bot library !
#
#

__version__ = 1

## imports

from .spc import Cfg, Db, Object
from .spc import get_kernel, os

from .obj import ENOCLASS
from .utl import cdir, list_files, get_cls, get_type

## classes

class Log(Object):

    pass

class Todo(Object):

    pass

## commands

def cfg(event):
    k = get_kernel()
    event.reply(k.cfg)

def icfg(event):
    from .irc import Cfg
    cfg = Cfg()
    cfg.last()
    if len(event.args) == 3:
        cfg.server, cfg.channel, cfg.nick = event.args
    elif len(event.args) == 2:
        cfg.server, cfg.channel = event.args
        cfg.nick = k.cfg.name
    elif len(event.args) == 1:
        cfg.server = event.args[0]
        cfg.channel = "#%s" % k.cfg.name
        cfg.nick = k.cfg.name
    event.reply(cfg)

def cmds(event):
    k = get_kernel()
    event.reply("|".join(sorted(k.cmds)))

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    got = []
    db = Db()
    for todo in db.find("bot.cmd.Todo", selector):
        todo._deleted = True
        todo.save()
        event.reply("ok")
        break

def ed(event):
    k = get_kernel()
    if not event.args:
        event.reply(list_files(k.cfg.workdir) or "no files yet")
        return
    k = get_kernel()
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
    l.edit(setter)
    l.save()
    event.reply("ok")

def find(event):
    import bot.obj
    k = get_kernel()
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
    k = get_kernel()
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def log(event):
    k = get_kernel()
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
    k = get_kernel()
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.cmd.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    p = o.save()
    event.reply("ok %s" % p)

def v(event):
    k = get_kernel()
    event.reply("%s %s" % (k.cfg.name.upper(), k.cfg.version))
