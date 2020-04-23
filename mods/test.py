# BOTLIB - Frameworkcto program bots
#
#

import bot
import sys

from lo.thr import get_name

k = bot.get_kernel()

def test1(event):
    bot = k.fleet.by_orig(event.orig)
    try:
        bot._sock.shutdown(2)
        event.reply("closed socked on %s" % get_name(bot))
    except AttributeError:
        pass
    try:
        sys.stdin.shutdown(2)
    except Exception as ex:
        pass