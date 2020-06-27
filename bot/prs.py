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
        super().__init__()
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
        super().__init__()
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post
                    
def parse(o, txt):
    n = type(o)()
    args = []
    opts = []
    n.gets = Default()
    n.opts = Default()
    n.sets = Default()
    for token in [Token(txt) for txt in txt.split()]:
        g = Getter(token.txt)
        if g:
            n.gets.update(g)
            continue
        s = Setter(token.txt)
        if s:
            n.sets.update(s)
            continue
        opt = Option(token.txt)
        if opt.opt:
            n.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        return
    n.cmd = args[0]
    n.args = args[1:]
    n.txt = " ".join(args)
    n.rest = " ".join(args[1:])
    return n