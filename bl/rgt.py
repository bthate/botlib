# BOTLIB - Framework to program bots.
#
# 

import bl

def __dir__():
    return ("Register")

class Register(bl.pst.Persist):

    def get(self, k):
        return bl.get(self, k)

    def register(self, k, v):
        bl.set(self, k, v)
