# This file is placed in the Public Domain.

from .dbs import find, listfiles
from .mbx import to_date
from .nms import Names
from .obj import cfg, fmt, opts
from .tms import elapsed, fntime
from .zzz import os, time

def fnd(event):
    if not event.args:
        fls = listfiles(cfg.wd)
        if fls:
            event.reply("|".join([x.split(".")[-1].lower() for x in fls]))
        return
    name = event.args[0]
    t = Names.getnames(name)
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    for otype in t:
        for fn, o in find(otype, event.gets, event.index, event.timed):
            nr += 1
            txt = "%s %s" % (str(nr), fmt(o, args or o.keys(), skip=event.skip.keys()))
            if opts("t") or "t" in event.opts:
                if "Date" in o.keys():
                    fn = os.sep.join(to_date(o.Date).split())
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
