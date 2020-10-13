# OLIB - object library
#
#

import ol

classes = ol.Object()
mods = ol.Object()
funcs = ol.Object()
names = ol.Object()

ol.update(classes, {"Bus": ["ol.bus"], "Cfg": ["mymod.rss"], "Console": ["ol.csl"], "DCC": ["bot.irc"], "Email": ["mymod.mbx"], "Event": ["bot.irc"], "Feed": ["mymod.rss"], "Fetcher": ["mymod.rss"], "Getter": ["ol.prs"], "Handler": ["ol.hdl"], "IRC": ["bot.irc"], "Kernel": ["ol.krn"], "Loader": ["ol.ldr"], "Log": ["mymod.ent"], "Option": ["ol.prs"], "Repeater": ["ol.tms"], "Rss": ["mymod.rss"], "Seen": ["mymod.rss"], "Setter": ["ol.prs"], "Skip": ["ol.prs"], "Timed": ["ol.prs"], "Timer": ["ol.tms"], "Todo": ["mymod.ent"], "Token": ["ol.prs"], "UDP": ["bmod.udp"], "User": ["bot.irc"], "Users": ["bot.irc"]})

ol.update(mods, {"cfg": "bmod.cfg", "cmd": "bmod.cmd", "cor": "mymod.mbx", "dne": "mymod.ent", "dpl": "mymod.rss", "edt": "mymod.edt", "eml": "mymod.mbx", "fed": "mymod.rss", "fnd": "bmod.fnd", "ftc": "mymod.rss", "krn": "mymod.dbg", "log": "mymod.ent", "mbx": "mymod.mbx", "mds": "mymod.dbg", "rm": "mymod.rss", "rss": "mymod.rss", "sts": "mymod.sts", "tbl": "mymod.dbg", "tdo": "mymod.ent", "tsk": "bmod.cmd", "upt": "bmod.cmd", "ver": "bmod.cmd"})

ol.update(funcs, {"cfg": "bmod.cfg.cfg", "cmd": "bmod.cmd.cmd", "cor": "mymod.mbx.cor", "dne": "mymod.ent.dne", "dpl": "mymod.rss.dpl", "edt": "mymod.edt.edt", "eml": "mymod.mbx.eml", "fed": "mymod.rss.fed", "fnd": "bmod.fnd.fnd", "ftc": "mymod.rss.ftc", "krn": "mymod.dbg.krn", "log": "mymod.ent.log", "mbx": "mymod.mbx.mbx", "mds": "mymod.dbg.mds", "rm": "mymod.rss.rm", "rss": "mymod.rss.rss", "sts": "mymod.sts.sts", "tbl": "mymod.dbg.tbl", "tdo": "mymod.ent.tdo", "tsk": "bmod.cmd.tsk", "upt": "bmod.cmd.upt", "ver": "bmod.cmd.ver"})

ol.update(names, {"bus": ["ol.bus.Bus"], "cfg": ["mymod.rss.Cfg"], "console": ["ol.csl.Console"], "dcc": ["bot.irc.DCC"], "email": ["mymod.mbx.Email"], "event": ["bot.irc.Event"], "feed": ["mymod.rss.Feed"], "fetcher": ["mymod.rss.Fetcher"], "getter": ["ol.prs.Getter"], "handler": ["ol.hdl.Handler"], "irc": ["bot.irc.IRC"], "kernel": ["ol.krn.Kernel"], "loader": ["ol.ldr.Loader"], "log": ["mymod.ent.Log"], "option": ["ol.prs.Option"], "repeater": ["ol.tms.Repeater"], "rss": ["mymod.rss.Rss"], "seen": ["mymod.rss.Seen"], "setter": ["ol.prs.Setter"], "skip": ["ol.prs.Skip"], "timed": ["ol.prs.Timed"], "timer": ["ol.tms.Timer"], "todo": ["mymod.ent.Todo"], "token": ["ol.prs.Token"], "udp": ["bmod.udp.UDP"], "user": ["bot.irc.User"], "users": ["bot.irc.Users"]})
