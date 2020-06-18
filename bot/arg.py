# BOTLIB - the bot library
#
#

from .obj import O, Object

class Arg(O):

    def __init__(self, txt):
        self._txt = txt
        try:
            self.pre, self.post = self._txt.split("=")
        except ValueError:
            self.pre = self.post = ""
                    
class Args(Object):

    def __init__(self, txt):
        super().__init__()
        self._txt = txt
        nr = 0
        for l in self._txt.split():
            if l:
                self[str(nr)] = Arg(l)
                nr += 1

    def __iter__(self):
        for nr in range(len(self)):
            if type(nr) == int:
                try:
                    yield self[str(nr)]
                except KeyError:
                    pass


class Options(Object):

    def __init__(self, txt):
        super().__init__()
        for arg in Args(txt):
            if arg.pre:
                self[arg.pre] = arg.post
