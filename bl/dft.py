# BOTLIB - Framework to program bots.
#
# 

import bl.pst

from bl.obj import get, set, update

def __dir__():
    return ("Default", )

class Default(bl.pst.Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            update(self, cfg)

    def __getattr__(self, k):
        if not k in self:
            set(self, k, "")
        return get(self, k)
