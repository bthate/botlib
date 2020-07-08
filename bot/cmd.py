# BOTLIB - the bot library !
#
#

import time

from .irc import Cfg
from .krn import k, starttime, __version__
from .obj import get, last, save, tostr, update
from .prs import parse
from .tms import elapsed

def __dir__():
    return ("cfg", "cmds", "meet", "up", "v")

def cfg(event):
    c = Cfg()
    last(c)
    parse(event, event.txt)
    if event.sets:
        update(c, event.sets)
        save(c)
    event.reply(tostr(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

def meet(event):
    if not event.args:
        event.reply("meet <userhost>")
        return
    origin = event.args[0]
    origin = get(k.users.userhosts, origin, origin)
    k.users.meet(origin)
    event.reply("ok")

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("%s %s" % ("BOTLIB", __version__))
