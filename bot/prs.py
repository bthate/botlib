# BOTLIB - the bot library
#
#

from .obj import O, Object, Default

class Token(O):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt
        try:
            self.pre, self.post = self.txt.split("==")
        except ValueError:
            self.pre = self.post = ""
        try:
            self.key, self.value = self.txt.split("=")
        except ValueError:
            self.key = self.value = ""
                    
class Parsed(Object):

    def __init__(self):
        super().__init__()

    def parse(self, txt):
        if not txt:
            return
        self.txt = txt
        self.args = []
        self.gets = Default()
        self.sets = Default()
        tokens = [Token(x) for x in txt.split()]
        for token in tokens:
            if token.pre:
                self.gets[token.pre] = token.post
            elif token.set:
                self.sets[token.set] = token.post
            else:
                self.args.append(token.txt)
        self.rest = " ".join(self.args)
        self.cmd = tokens[0].txt