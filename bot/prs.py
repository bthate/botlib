# BOTLIB - the bot library
#
#

import os, sys

from .dct import Dict
from .dft import Default
from .krn import Cfg, k
from .obj import Object
from .utl import update

def __dir__():
    return ("parse", "parse_cli")

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
    args = []
    opts = []
    o.origtxt = txt
    o.gets = Dict()
    o.opts = Dict()
    o.sets = Dict()
    for token in [Token(txt) for txt in txt.split()]:
        g = Getter(token.txt)
        if g:
            o.gets.update(g)
            continue
        s = Setter(token.txt)
        if s:
            o.sets.update(s)
            o.update(s)
            continue
        opt = Option(token.txt)
        if opt.opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            o.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o

def parse_cli(name="bot"):
    if root():
        p = "/var/lib/%s" % name
    else:
        p = os.path.expanduser("~/.%s" % name)
    import bot.pst
    bot.pst.workdir = p
    if len(sys.argv) <= 1:
        c = Cfg()
        parse(c, "")
        return c
    c = Cfg()
    parse(c, " ".join(sys.argv[1:]))
    k.cfg.update(c)
    return c

def root():
    if os.geteuid() != 0:
        return False
    return True
