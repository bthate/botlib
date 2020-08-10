# BOTLIB - the bot library
#
#

from .obj import Object

class Default(Object):

    def __getattr__(self, k):
        if k not in self:
            return ""
        return self.__dict__[k]
