# This file is in the Public Domain.

__version__ = 120

def register():
    Names.add(ver)

def ver(event):
    from obj import cfg
    event.reply("%s %s" % (cfg.name.upper(), cfg.version))
