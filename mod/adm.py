# This file is in the Public Domain.

import sys
import threading
import time

from hdl import Bus
from obj import Object, Names, edit, fmt, getname
from run import kernel
from tms import elapsed

def register():
    Names.add(flt)
    Names.add(krn)
    Names.add(thr)
    Names.add(upt)

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(fmt(Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def krn(event):
    k = kernel() 
    if not event.args:
        event.reply(fmt(k.cfg, skip=["opts", "sets", "old", "res"]))
        return
    edit(k.cfg, event.sets)
    p = k.cfg.save()
    event.reply("ok")

def thr(event):
    k = kernel()
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        o.update(vars(thr))
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - k.starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def upt(event):
    k = kernel()
    event.reply("uptime is %s" % elapsed(time.time() - k.starttime))
