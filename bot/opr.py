# BOTLIB - the bot library !
#
#

import os, threading, time
import bot.obj

from .dbs import Db, last
from .err import ENOCLASS
from .irc import Cfg
from .isp import find_shorts
from .krn import k, starttime
from .obj import Object, format, get, keys, save, update
from .prs import parse
from .tms import elapsed, fntime
from .utl import cdir, get_cls, get_type

def __dir__():
    return ("cfg", "edt", "fnd", "flt", "krn", "tsk", "upt", "ver", "wd")

def cfg(event):
    c = Cfg()
    last(c)
    parse(event, event.txt)
    if event.sets:
        update(c, event.sets)
        save(c)
    event.reply(format(c))

def edit(o, setter, skip=False):
    try:
        setter = vars(setter)
    except (TypeError, ValueError):
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        if skip and value == "":
            continue
        count += 1
        if value in ["True", "true"]:
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
    return count

def list_files(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return ""
    return "|".join(os.listdir(path))

def edt(event):
    if not event.args:
        event.reply(list_files(bot.obj.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = find_shorts("bot")
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

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def krn(event):
    event.reply(k)

def tsk(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Object()
        update(o, d)
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res:
            event.reply(res.rstrip())

def upt(event):
    event.reply(elapsed(time.time() - starttime))

def ver(event):
    from bot.krn import __version__
    event.reply("BOTLIB %s" % __version__)
    for mod in k.walk("bot"):
        try:
            event.reply("%s %s" % (mod.__name__, mod.__version__))
        except AttributeError:
            continue

def wd(event):
    event.reply(bot.obj.workdir)
