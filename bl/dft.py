# BOTLIB - Framework to program bots.
#
# 

import bl

def __dir__():
    return ("Default", )

class Default(bl.pst.Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            bl.update(self, cfg)

    def __getattr__(self, k):
        if not k in self:
            bl.set(self, k, "")
        return bl.get(self, k)
