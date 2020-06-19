# BOTLIB - the bot library
#
#

from .obj import O, Object, Default

class Token(O):

    def __init__(self, txt):
        self.txt = txt

class Getter(O):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
        
class Setter(O):

    def __init__(self, txt):
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
                    
class Parsed(Default):

    def parse(self, txt):
        if not txt:
            return
        self.txt = txt
        self.args = []
        self.gets = Default()
        self.sets = Default()
        tokens = [Token(txt) for txt in txt.split()]
        nr = -1
        for token in tokens:
            nr += 1
            if not token.txt:
                continue
            self.gets.update(Getter(token.txt))
            self.sets.update(Setter(token.txt))            
            if nr and "=" not in token.txt:
                self.args.append(token.txt)
        self.rest = " ".join(self.args)
        self.cmd = tokens[0].txt