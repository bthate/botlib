# BOTLIB - the bot library !
#
#

from .irc import IRC

def cfg(event):
    i = IRC()
    i.cfg.last()
    try:
        i.server, i.channel, i.nick = event.args
        i.save()
        event.reply("ok")
    except:
        event.reply(i.cfg)
