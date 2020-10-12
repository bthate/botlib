# BOTLIB - the bot library !
#
#

import ol

def krn(event):
    event.reply(ol.ojson(k))

def mds(event):
    mods = ol.utl.find_modules("bmod")
    event.reply(",".join([m.__name__ for m in mods]))

def tbl(event):
    from ol.tbl import classes, mods, funcs, names
    event.reply("classes = %s" % classes)
    event.reply("mods = %s" % mods)
    event.reply("funcs = %s" % funcs)
    event.reply("classes = %s" % classes)
