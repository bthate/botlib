# BOTLIB - Frameworkcto program bots
#
#

from bot import k
from lo.thr import get_name

def test1(event):
    bot = k.fleet.by_orig(event.orig)
    try:
        bot._sock.shutdown(2)
        event.reply("closed socked on %s" % get_name(bot))
    except AttributeError:
        pass
