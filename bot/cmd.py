# This file is in the Public Domain.

from .nms import Names

def cmd(event):
    event.reply(",".join(sorted(Names.modules.keys())))

def ech(event):
    if event.rest:
        event.reply(event.rest)
