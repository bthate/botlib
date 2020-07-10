# BOTLIB - the bot library !
#
#

import time

from .irc import Cfg
from .krn import k, starttime, __version__
from .prs import parse
from .tms import elapsed
from .utl import tostr

def __dir__():
    return ("cfg", "cmds")

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
