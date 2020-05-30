# BOTLIB- Framework to program bots.
#
#

""" configure the bot. """

import bot
import bot.lib
import bot.irc

def __dir__():
    return ("cfg", )

def cfg(event):
    owner = None
    try:
        server, channel, nick, owner = event.args
    except ValueError:
        try:
            server, channel, nick = event.args
        except ValueError:
            event.reply("cfg <server> <channel> <nick> [<owner>]")
            return
    k = bot.lib.get_kernel()
    c = bot.irc.Cfg()
    c.last()
    c.server = server
    c.channel = channel
    c.nick = nick
    c.save()
    if owner:
        cc = bot.lib.krn.Cfg()
        cc.last()
        cc.owner = owner
        cc.save()
        k.users.meet(owner)
    event.reply("ok")
