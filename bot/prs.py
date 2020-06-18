# BOTLIB - the bot library
#
#

from .obj import O, Default

class Token(O):

    def __init__(self, txt):
        self.txt = txt
        try:
            self.pre, self.post = self.txt.split("==")
        except ValueError:
            self.pre = self.post = ""
        try:
            self.set, self.post = self.txt.split("=")
        except ValueError:
            self.pre = self.post = ""
                    
class Parsed(Default):

    def parse(self, txt):
        if not txt:
            return
        self.txt = txt
        self.args = []
        self.opts = Default()
        self.set = Default()
        tokens = [Token(x) for x in txt.split()]
        nr = -1
        for token in tokens:
            nr += 1
            if nr == 0:
                self.cmd = token.txt
                continue
            if token.pre:
                self.opts[token.pre] = token.post
            elif token.set:
                self.set[token.set] = token.post
            else:
                self.args.append(token.txt)
        self.rest = " ".join(self.args)
        self.cmd = tokens[0].txt
