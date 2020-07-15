# BOTLIB - the bot library !
#
#

from .krn import k

def __dir__():
    return ("cmd",)

def cmd(event):
    event.reply("|".join(sorted(k.cmds)))
