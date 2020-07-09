# BOTLIB - the bot library !
#
#

import time

from .irc import Cfg
from .krn import k, starttime, __version__
from .obj import tostr
from .prs import parse
from .tms import elapsed

def __dir__():
    return ("cfg", "cmds", "up", "v")

def cfg(event):
    c = Cfg()
    c.last()
    parse(event, event.txt)
    if event.sets:
        c.update(event.sets)
        c.save()
    event.reply(tostr(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("%s %s" % ("BOTLIB", __version__))
