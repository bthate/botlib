# This file is in the Public Domain.

import sys
import threading
import time

from bus import Bus
from edt import edit
from nms import Names
from obj import Object, fmt, getname, starttime
from tms import elapsed

def register():
    Names.add(cmd)
    Names.add(flt)
    Names.add(krn)
    Names.add(thr)
    Names.add(upt)
    Names.add(ver)

def cmd(event):
    event.reply(",".join(sorted(Names.modules)))

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(str(Bus.objs[index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def krn(event):
    from obj import cfg
    if not event.args:
        event.reply(fmt(cfg, skip=["opts", "sets", "old", "res"]))
        return
    edit(cfg, s)
    p = cfg.save()
    print(p)
    event.reply("ok")

def thr(event):
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
            up = int(time.time() - starttime)
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
    event.reply("uptime is %s" % elapsed(time.time() - starttime))

def ver(event):
    from obj import cfg
    event.reply("%s %s" % (cfg.name.upper(), cfg.version))
