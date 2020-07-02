# BOTLIB - the bot library
#
#

__version__ = 87

import time

from bot.csl import execute
from bot.krn import k
from bot.prs import parse_cli

def __dir__():
    return ("execute", "k", "starttime", "parse_cli")

starttime = time.time()
