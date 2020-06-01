# BOTLIB - Framework to program bots.
#
#

""" default values. """

import lo

#:
default_irc = {
    "channel": "#%s" % (lo.cfg.name or "botd"),
    "nick": lo.cfg.name or "botd",
    "ipv6": False,
    "port": 6667,
    "server": "localhost",
    "ssl": False,
    "realname": lo.cfg.name or "botd",
    "username": lo.cfg.name or "botd"
}

#:
default_krn = {
    "workdir": "",
    "kernel": False,
    "modules": "",
    "options": "",
    "prompting": True,
    "dosave": False,
    "level": "",
    "logdir": "",
    "shell": False
}

#:
default_rss = {
    "display_list": "title,link",
    "dosave": True,
    "tinyurl": False
}

#:
defaults = lo.Object()
defaults["bot.irc.Cfg"] = lo.Object(default_irc)
defaults["bot.rss.Cfg"] = lo.Object(default_rss)
defaults["lo.krn.Cfg"] = lo.Object(default_krn)
