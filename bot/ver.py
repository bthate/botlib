# This file is placed in the Public Domain.

from .krn import Kernel

def ver(event):
    event.reply("%s %s" % (Kernel.cfg.name.upper(), Kernel.cfg.version))
