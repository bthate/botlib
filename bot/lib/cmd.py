# BOTLIB - Framework to program bots.
#
#

""" object editor. """

import bot.lib as lib
import os

def __dir__():
    return ("ed", "find")

def ed(event):
    """ edit the last saved object of a type. """
    assert(lib.workdir)
    if not event.args:
        files = [x for x in os.listdir(os.path.join(lib.workdir, "store"))]
        if files:
            event.reply("|".join(list(files)))
        return
    cn = event.args[0]
    db = lib.Db()
    l = db.last(cn)
    if not l:     
        c = lib.typ.get_cls(cn)
        l = c()
        event.reply("created %s" % cn)
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    p = l.save()
    event.reply("ok %s" % p)

def find(event):
    """ locate objects on disk. """
    if not event.args:
        wd = os.path.join(lib.workdir, "store", "")
        lib.cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0].split(".")[-1].lower() for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    k = lib.get_kernel()
    shorts = k.find_shorts()
    db = lib.Db()
    otypes = []
    target = db.all
    otype = event.args[0]
    otypes = shorts.get(otype, [otype,])
    try:
       match = event.args[1]
       target = db.find_value
    except:
       match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for ot in otypes:
        for o in target(ot, match):
            nr += 1
            event.display(o, str(nr), args or o.keys())
    if nr == -1:
        event.reply("no %s objects." % "|".join(otypes))
