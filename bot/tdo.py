# This file is in the Public Domain.

from ob import Object, save
from ob.dbs import find

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("obm.tdo.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break
