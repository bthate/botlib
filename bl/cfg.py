# BOTLIB - Framework to program bots.
#
# 

import bl
import bl.pst

from bl import k
from bl.obj import update

def __dir__():
    return ("Cfg",)

class Cfg(bl.pst.Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            update(self, cfg)

def cfg(event):
    if not event.args:
        event.reply(k.cfg)
        return
    try:
        bl.last(k.cfg)
        bl.obj.set(k.cfg, event.args[0], event.args[1])
        k.cfg.save()
        event.reply("ok")
    except IndexError:
        event.reply("cfg %s value" % "|".join(bl.obj.keys(k.cfg)))
