# BOTLIB - the bot library !
#
#

from .krn import k

def __dir__():
    return ("cmds",)

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))
