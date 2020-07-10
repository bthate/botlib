# BOTLIB - the bot library !
#
#

import time

from .dbs import last
from .irc import Cfg
from .krn import k, starttime, __version__
from .prs import parse
from .tms import elapsed
from .utl import tostr, update

def __dir__():
    return ("cfg", "cmds")

def cfg(event):
    c = Cfg()
    last(c)
    parse(event, event.txt)
    if event.sets:
        update(c, event.sets)
        c.__save__()
    event.reply(tostr(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))
