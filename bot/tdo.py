# This file is in the Public Domain.

from bot.dbs import find
from bot.nms import Names
from bot.obj import Object

def init():
    Names.add(dne)
    Names.add(tdo)

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        event.reply("dne txt==<string>")
        return
    for fn, o in find("todo", event.gets):
        o._deleted = True
        o.save()
        event.reply("ok")
        break

def tdo(event):
    if not event.rest:
        event.reply("tdo <txt>")
        return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
