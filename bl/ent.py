# BOTLIB - Framework to program bots.
#
# 

import bl

def __dir__() -> tuple:
    return ("Log", "Todo", "log", "todo")

class Log(bl.pst.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(bl.pst.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
        nr = 0
        if not event.dkeys:
            event.dkeys.append("txt")
        for o in bl.k.db.find("bl.ent.Log", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
        nr = 0
        if "txt" not in event.dkeys:
            event.dkeys.append("txt")
        for o in bl.k.db.find("bl.ent.Todo", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
