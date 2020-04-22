# BOTLIB - Framework to program bots.
#
#

__version__ = 80

import bot.krn
import time

def __dir__():
    return ("dft", "ent", "flt", "fnd", "irc", "krn", "rss", "shw", "udp",  "usr")

#:
starttime = time.time()

#:
k = bot.krn.Kernel()
