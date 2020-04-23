# BOTLIB - Framework to program bots.
#
#

__version__ = 80

import lo
import time

def __dir__():
    return ("dft", "ent", "flt", "fnd", "get_kernel", "irc", "kernel", "krn", "rss", "shw", "udp",  "usr")

#:
starttime = time.time()

#:
kernels = []

def get_kernel(nr=0):
    return kernels[nr]
   