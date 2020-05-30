# BOTLIB - Framework to program bots.
#
#

""" show runtime stats. """

import os
import pkg_resources
import threading
import time

from . import Object, get_kernel, starttime
from .typ import get_type, get_cls
from .tms import elapsed

def __dir__():
    return ("cfg", "cmds", "fleet", "mods", "ps", "types", "up", "v")

k = get_kernel()

def cfg(event):
    assert(lib.workdir)
    l = lib.cfg
    if not event.args:
        event.reply(l)
        return
    if len(event.args) == 1:
        event.reply(l.get(event.args[0]))
        return
    setter = {event.args[0]: event.args[1]}
    l.edit(setter)
    event.reply(l)

def cmds(event):
    k = get_kernel()
    b = k.fleet.by_orig(event.orig)
    if b and b.cmds:
        event.reply("|".join(sorted(b.cmds)))

def fleet(event):
    k = get_kernel()
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def mods(event):
    fns = []
    k = get_kernel()
    modnames = k.cfg.modules.split(",")
    if not modnames:
        modsnames = ["bot"]
    for modname in modnames:
        if not modname:
            continue
        modname = modname.split(".")[0]
        fns = pkg_resources.resource_listdir(modname, "")
        event.reply("|".join(["%s.%s" % (modname, fn[:-3]) for fn in fns if not fn.startswith("_") and fn.endswith(".py")]))

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Object()
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
        if res.strip():
            event.reply(res)

def types(event):
    k = lib.get_kernel()
    res = []
    for mod in k.find_modules():
        for t in k.find_types(mod):
            if t not in res:
               res.append(t)
    if res:
        event.reply("|".join(sorted(res, key=lambda x: x not in res)))

def up(event):
    event.reply(lib.tms.elapsed(time.time() - starttime))

def v(event):
    n = k.cfg.name or "botlib"
    v = k.cfg.version or __version__
    event.reply("%s %s" % (n.upper(), v))
