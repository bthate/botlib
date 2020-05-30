# BOTLIB - Framework to program bots.
#
#

""" user management. """

import bot
import lo

k = lo.get_kernel()

def meet(event):
    if not event.origin == k.cfg.owner:
        event.reply("only owner can add users")
        return
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = bot.usr.Users.userhosts.get(origin, origin)
    k.users.meet(origin, perms)
    event.reply("ok")

def users(event):
    res = ""
    db = Db()
    for o in db.all("bot.usr.User"):
        res += "%s," % o.user
    event.reply(res)
