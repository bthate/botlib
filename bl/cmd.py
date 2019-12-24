# BOTLIB - Framework to program bots.
#
# basic commands. 

import bl

class Log(bl.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(bl.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

def cfg(event):
    if not event.args:
        event.reply(bl.cfg)
        return
    if len(event.args) >= 1:
        cn = "bl.%s.Cfg" % event.args[0]
        l = bl.db.last(cn)
        if not l:
            event.reply("no %s config found." % event.args[0])
            return
        if len(event.args) == 1:
            event.reply(l)
            return
        if len(event.args) == 2:
            event.reply(bl.get(l, event.args[1]))
            return
        bl.set(l, event.args[0], event.args[1])
        bl.cfg.save()
        event.reply("ok")

def log(event):
    if not event.rest:
        nr = 0
        if not event.dkeys:
            event.dkeys.append("txt")
        for o in bl.db.find("bl.cmd.Log", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = bl.get(bl.users.userhosts, origin, origin)
    u = bl.users.meet(origin, perms)
    event.reply("added %s" % u.user)

def todo(event):
    if not event.rest:
        nr = 0
        if "txt" not in event.dkeys:
            event.dkeys.append("txt")
        for o in bl.db.find("bl.cmd.Todo", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
