# BOTLIB - the bot library
#
#

from .obj import O, Object

class Arg(O):

    def __init__(self, txt):
        self.txt = txt
        try:
            self.pre, self.post = txt.split("=")
        except ValueError:
            self.pre = self.post = ""
                    
class Args(Object):

    def __init__(self, txt):
        super().__init__()
        nr = 0
        for l in txt.split():
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
        self.parse()

    def parse(self):
        for arg in self:
            print(arg)
       