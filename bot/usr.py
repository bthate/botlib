# This file is in the Public Domain.

from ob import save
from ob.dbs import find
from ob.usr import User

def dlt(event):
    if not event.args:
        return
    selector = {"user": event.args[0]}
    for fn, o in find("usr.User", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def met(event):
    if not event.args:
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")
