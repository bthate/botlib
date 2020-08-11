# BOTLIB - the bot library !
#
#

import os, sys, time
import bot.obj

from .dbs import Db
from .obj import get, format, keys
from .prs import parse
from .tms import elapsed, fntime
from .isp import find_shorts
from .utl import cdir

def fnd(event):
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
    otype = event.args[0]
    shorts = find_shorts("bot")
    otypes = get(shorts, otype, [otype,])
    args = list(keys(event.gets))
    try:
        arg = event.args[1:]
    except ValueError:
        arg = []
    args.extend(arg)
    nr = -1
    for otype in otypes:
        for o in db.find(otype, event.gets, event.index, event.timed):
            nr += 1
            if "f" in event.opts:
                pure = False
            else:
                pure = True
            txt = "%s %s" % (str(nr), format(o, args, pure))
            if "t" in event.opts:
                txt += " %s" % (elapsed(time.time() - fntime(o.__stamp__)))
            event.reply(txt)
    if nr == -1:
        event.reply("no matching objects found.")

