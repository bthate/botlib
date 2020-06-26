# BOTLIB - the bot library
#
#

from .obj import Object, Default

class Token(Object):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

class Option(Default):

    def __init__(self, txt):
        if txt.startswith("--"):
            self.opt = txt[2:]
        if txt.startswith("-"):
            self.opt = txt[1:]

class Getter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
        
class Setter(Object):

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
        self.gets = Default()
        self.options = []
        self.sets = Default()
        args = []
        tokens = [Token(txt) for txt in txt.split()]
        for token in tokens:
            g = Getter(token.txt)
            if g:
                self.gets.update(g)
                continue
            s = Setter(token.txt)
            if s:
                self.sets.update(s)
                continue
            o = Option(token.txt)
            if o.opt:
                self.options.append(o.opt)
                continue
            args.append(token.txt)
        self.txt =  " ".join(args)
        tokens = [Token(txt) for txt in args]
        nr = -1
        for token in tokens:
            nr += 1
            if nr == 0:
                self.cmd = token.txt
                continue
            self.args.append(token.txt)
        self.rest = " ".join(self.args)
