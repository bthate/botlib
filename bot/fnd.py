# This file is placed in the Public Domain.

import time

from ob import cfg, format, keys, op
from ob.bus import by_orig
from ob.dbs import find, list_files
from ob.prs import elapsed
from ob.utl import fntime

def fnd(event):
    if not event.args:
        fls = list_files(cfg.wd)
        if fls:
            event.reply("|".join([x.split(".")[-1].lower() for x in fls]))
        return
    name = event.args[0]
    bot = by_orig(event.orig)
    t = bot.get_names(name)
    nr = -1
    for otype in t:
        for fn, o in find(otype, event.gets, event.index, event.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, keys(o), skip=event.skip))
            if op("t"):
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
