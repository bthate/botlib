# This file is placed in the Public Domain.

from .obj import Default, Object
from .itr import findall, findmods, findnames
from .utl import direct

class Names(Object):

    names = Default({
        "bus": [
            "bot.bus.Bus"
        ],
        "cfg": [
            "bot.obj.Cfg",
            "bot.rss.Cfg",
            "bot.udp.Cfg",
            "bot.irc.Cfg"
        ],
        "client": [
            "bot.hdl.Client"
        ],
        "command": [
            "bot.evt.Command"
        ],
        "dcc": [
            "bot.irc.DCC"
        ],
        "default": [
            "bot.obj.Default"
        ],
        "email": [
            "bot.mbx.Email"
        ],
        "enoclass": [
            "bot.err.ENOCLASS"
        ],
        "enofilename": [
            "bot.err.ENOFILENAME"
        ],
        "enomore": [
            "bot.err.ENOMORE"
        ],
        "enotimplemented": [
            "bot.err.ENOTIMPLEMENTED"
        ],
        "enotxt": [
            "bot.err.ENOTXT"
        ],
        "enouser": [
            "bot.err.ENOUSER"
        ],
        "event": [
            "bot.evt.Event",
            "bot.irc.Event"
        ],
        "feed": [
            "bot.rss.Feed"
        ],
        "fetcher": [
            "bot.rss.Fetcher"
        ],
        "getter": [
            "bot.prs.Getter"
        ],
        "handler": [
            "bot.hdl.Handler"
        ],
        "httperror": [
            "urllib.error.HTTPError"
        ],
        "irc": [
            "bot.irc.IRC"
        ],
        "loader": [
            "bot.ldr.Loader"
        ],
        "log": [
            "bot.log.Log"
        ],
        "names": [
            "bot.nms.Names"
        ],
        "o": [
            "bot.obj.O"
        ],
        "obj": [
            "bot.obj.Obj"
        ],
        "object": [
            "bot.obj.Object"
        ],
        "objectlist": [
            "bot.obj.ObjectList"
        ],
        "option": [
            "bot.prs.Option"
        ],
        "output": [
            "bot.opt.Output"
        ],
        "repeater": [
            "bot.clk.Repeater"
        ],
        "request": [
            "urllib.request.Request"
        ],
        "rss": [
            "bot.rss.Rss"
        ],
        "seen": [
            "bot.rss.Seen"
        ],
        "setter": [
            "bot.prs.Setter"
        ],
        "skip": [
            "bot.prs.Skip"
        ],
        "textwrap": [
            "bot.irc.TextWrap"
        ],
        "thr": [
            "bot.thr.Thr"
        ],
        "timed": [
            "bot.prs.Timed"
        ],
        "timer": [
            "bot.clk.Timer"
        ],
        "todo": [
            "bot.tdo.Todo"
        ],
        "token": [
            "bot.prs.Token"
        ],
        "udp": [
            "bot.udp.UDP"
        ],
        "urlerror": [
            "urllib.error.URLError"
        ],
        "user": [
            "bot.usr.User"
        ],
        "users": [
            "bot.usr.Users"
        ]
    })

    modules = Object({
        "cfg": "bot.irc",
        "cmd": "bot.cmd",
        "dlt": "bot.usr",
        "dne": "bot.tdo",
        "dpl": "bot.rss",
        "ech": "bot.adm",
        "flt": "bot.adm",
        "fnd": "bot.fnd",
        "ftc": "bot.rss",
        "krn": "bot.adm",
        "log": "bot.log",
        "mbx": "bot.mbx",
        "met": "bot.usr",
        "rem": "bot.rss",
        "rss": "bot.rss",
        "sve": "bot.adm",
        "tdo": "bot.tdo",
        "thr": "bot.adm",
        "upt": "bot.adm"
    })

    inits =  Object({
        "adm": "bot.adm",
        "bus": "bot.bus",
        "clk": "bot.clk",
        "dbs": "bot.dbs",
        "edt": "bot.edt",
        "err": "bot.err",
        "evt": "bot.evt",
        "fnd": "bot.fnd",
        "hdl": "bot.hdl",
        "irc": "bot.irc",
        "itr": "bot.itr",
        "ldr": "bot.ldr",
        "log": "bot.log",
        "mbx": "bot.mbx",
        "nms": "bot.nms",
        "obj": "bot.obj",
        "opt": "bot.opt",
        "prs": "bot.prs",
        "rss": "bot.rss",
        "tdo": "bot.tdo",
        "thr": "bot.thr",
        "tms": "bot.tms",
        "trc": "bot.trc",
        "trm": "bot.trm",
        "udp": "bot.udp",
        "url": "bot.url",
        "usr": "bot.usr",
        "utl": "bot.utl",
        "zzz": "bot.zzz"
    })

    @staticmethod
    def getnames(nm, dft=None):
        return Names.names.get(nm, dft)


    @staticmethod
    def getmodule(mn):
        return Names.modules.get(mn, None)

    @staticmethod
    def getinit(mn):
        return Names.inits.get(mn, None)

    @staticmethod
    def tbl(tbl):
        Names.names.update(tbl["names"])
        Names.modules.update(tbl["modules"])
        Names.inits.update(tbl["inits"])

    @staticmethod
    def walk(names):
        for mn in findall(names):
            mod = direct(mn)
            if "cmd" not in mn:
                Names.inits[mn.split(".")[-1]] = mn
            Names.modules.update(findmods(mod))
            for k, v in findnames(mod).items():
                if k not in Names.names:
                    Names.names[k] = []
                if v not in Names.names[k]:
                    Names.names[k].append(v)
