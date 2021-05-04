# This file is in the Public Domain.

__version__ = 120

from nms import Names
from run import kernel

def register():
    Names.add(ver)

def ver(event):
    k = kernel()
    event.reply("%s %s" % (k.cfg.name.upper(), k.cfg.version))
