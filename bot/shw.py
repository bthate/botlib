# BOTLIB - Framework to program bots.
#
#

""" show runtime stats. """

import bot
import bot.irc
import bot.krn
import lo
import lo.tms
import os
import pkg_resources
import threading
import time

def __dir__():
    return ("cmds", "fleet", "mods", "ps", "up", "v")

from bot.dft import defaults

def cmds(event):
    k = bot.get_kernel()
    b = k.fleet.by_orig(event.orig)
    if b.cmds:
        event.reply("|".join(sorted(b.cmds)))
    
def fleet(event):
    k = bot.get_kernel()
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([lo.typ.get_type(x) for x in k.fleet])

def mods(event):
    fns = pkg_resources.resource_listdir("bot", "")
    event.reply("|".join([".".join(fn.split(".")[:-1]) for fn in fns if not fn.startswith("_")]))

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = lo.Object()
        o.update(d)
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - bot.starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (lo.tms.elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def up(event):
    event.reply(lo.tms.elapsed(time.time() - bot.starttime))

def v(event):
    n = lo.cfg.name or "botlib"
    v = lo.cfg.version or bot.__version__
    event.reply("%s %s" % (n.upper(), v))
