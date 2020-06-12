# OKBOT - the ok bot !
#
# log text.

from .obj import Object
from .dbs import Db

def __dir__():
    return ("Log", 'log')

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("ok.log.Log", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Log()
    o.txt = event.rest
    o.save()
    event.reply("ok")
