# OLIB - object library
#
#

import ol

classes = ol.Object()
mods = ol.Object()
funcs = ol.Object()
names = ol.Object()

ol.update(classes, {"Bus": ["ol.bus"], "Cfg": ["bot.irc"], "Console": ["ol.csl"], "DCC": ["bot.irc"], "Event": ["bot.irc"], "Getter": ["ol.prs"], "Handler": ["ol.hdl"], "IRC": ["bot.irc"], "Kernel": ["ol.krn"], "Loader": ["ol.ldr"], "Option": ["ol.prs"], "Repeater": ["ol.tms"], "Setter": ["ol.prs"], "Skip": ["ol.prs"], "Timed": ["ol.prs"], "Timer": ["ol.tms"], "Token": ["ol.prs"], "UDP": ["bmod.udp"], "User": ["bot.irc"], "Users": ["bot.irc"]})

ol.update(mods, {"cfg": "bmod.cfg", "cmd": "bmod.cmd", "fnd": "bmod.fnd", "tsk": "bmod.cmd", "upt": "bmod.cmd", "ver": "bmod.cmd"})

ol.update(funcs, {"cfg": "bmod.cfg.cfg", "cmd": "bmod.cmd.cmd", "fnd": "bmod.fnd.fnd", "tsk": "bmod.cmd.tsk", "upt": "bmod.cmd.upt", "ver": "bmod.cmd.ver"})

ol.update(names, {"bus": ["ol.bus.Bus"], "cfg": ["bot.irc.Cfg"], "console": ["ol.csl.Console"], "dcc": ["bot.irc.DCC"], "event": ["bot.irc.Event"], "getter": ["ol.prs.Getter"], "handler": ["ol.hdl.Handler"], "irc": ["bot.irc.IRC"], "kernel": ["ol.krn.Kernel"], "loader": ["ol.ldr.Loader"], "option": ["ol.prs.Option"], "repeater": ["ol.tms.Repeater"], "setter": ["ol.prs.Setter"], "skip": ["ol.prs.Skip"], "timed": ["ol.prs.Timed"], "timer": ["ol.tms.Timer"], "token": ["ol.prs.Token"], "udp": ["bmod.udp.UDP"], "user": ["bot.irc.User"], "users": ["bot.irc.Users"]})
