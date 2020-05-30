# BOTLIB - Framework to program bots.
#
#

""" user entry commands (log/todo). """

from bot.ent import Log, Todo

def __dir__():
    return ("log", "todo", "done")

def log(event):
    """ log some text. """
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.ent.Log", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Log()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def todo(event):
    """ add a todo item. """
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("bot.ent.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def done(event):
    """ remove a todo item. """
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    got = []
    db = Db()
    for todo in db.find("bot.ent.Todo", selector):
        todo._deleted = True
        todo.save()
        event.reply("ok")
        break
