# BOTLIB - the bot library !
#
#

import os, threading, time
import bot.obj

from .cls import Dict
from .err import ENOCLASS
from .irc import Cfg
from .krn import k, starttime, __version__
from .obj import Db, last
from .prs import parse
from .isp import find_shorts
from .tms import elapsed
from .obj import cdir, get_cls, get_type

def __dir__():
    return ("cfg", "ed", "find", "fleet", "kernel", "ps", "up", "v")

def cfg(event):
    c = Cfg()
    last(c)
    parse(event, event.txt)
    if event.sets:
        c.update(event.sets)
        c.save()
    event.reply(c.format())

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

def ed(event):
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
    l.save()
    event.reply("ok")

def find(event):
    if not event.args:
        wd = os.path.join(bot.obj.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    parse(event, event.txt)
    db = Db()
    target = db.all
    otype = event.args[0]
    try:
        match = event.args[1]
        target = db.find
    except IndexError:
        match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for o in target(otype, event.gets):
        nr += 1
        txt = "%s %s" % (str(nr), o.format(event.args, True))
        if "t" in event.opts:
            txt += " %s" % (elapsed(time.time() - fntime(o.__stamp__)))
        event.reply(txt)
    if nr == -1:
        event.reply("no matching objects found.")

def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def kernel(event):
    event.reply(k)

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Dict()
        o.update(d)
        if o.get("sleep", None):
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

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("%s %s" % (k.cfg.name or "BOTLIB", __version__))
