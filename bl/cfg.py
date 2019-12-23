# BOTLIB - Framework to program bots.
#
# 

import bl

def __dir__():
    return ("Cfg",)

class Cfg(bl.pst.Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            bl.update(self, cfg)

def cfg(event):
    if not event.args:
        event.reply(bl.k.cfg)
        return
    try:
        bl.last(bl.k.cfg)
        bl.set(bl.k.cfg, event.args[0], event.args[1])
        bl.k.cfg.save()
        event.reply("ok")
    except IndexError:
        event.reply("cfg %s value" % "|".join(bl.keys(k.cfg)))
