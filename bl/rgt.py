# BOTLIB - Framework to program bots.
#
# 

import bl
import bl.pst

from bl.obj import get, set, update

def __dir__():
    return ("Register")

class Register(bl.pst.Persist):

    def get(self, k):
        return get(self, k)

    def register(self, k, v):
        set(self, k, v)
