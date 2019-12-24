# BOTLIB - Framework to program bots.
#
# 

import bl

def __dir__():
    return ("Cfg", "cfg")

class Cfg(bl.pst.Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            bl.update(self, cfg)

def cfg(event):
    if not event.args:
        event.reply(bl.k.cfg)
        return
    if len(event.args) >= 1:
        cn = "bl.%s.Cfg" % event.args[0]
        l = bl.k.db.last(cn)
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
        bl.k.cfg.save()
        event.reply("ok")
