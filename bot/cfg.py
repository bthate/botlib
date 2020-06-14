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
    except:
        event.reply(i.cfg)
        return
    event.reply("ok")
