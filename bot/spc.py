# BOTLIB - spc.py
#
# this file is placed in the public domain

"runtime objects"

# imports

from bot.hdl import Bus, Handler, cmd
from bot.rss import Fetcher

# defines

def __dir__():
    return ("bus", "fetcher", "h")

# runtime

bus = Bus()
fetcher = Fetcher()
h = Handler()
h.register("cmd", cmd)

