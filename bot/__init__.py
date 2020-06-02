# BOTLIB - Framework to program bots.
#
#

""" framework to program bots. """

__version__ = 84

import time

def __dir__():
    return ("cfg", "ent", "irc", "rss", "udp",  "starttime")

#:
starttime = time.time()

import bot.mods