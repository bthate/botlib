# BOTLIB - Framework to program bots.
#
#

__version__ = 80

import lo
import bot.krn
import time

from lo.shl import level, parse_cli
from bot.krn import Kernel

def __dir__():
    return ("dft", "ent", "flt", "fnd", "irc", "krn", "rss", "shw", "udp",  "usr")

#:
starttime = time.time()

#:
kernels = []

def get_kernel(nr=0):
    if not kernels:
        boot()
    return kernels[nr]
   