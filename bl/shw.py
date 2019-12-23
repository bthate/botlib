# BOTLIB - Framework to program bots.
#
# 

import os
import time
import threading
import bl

def show(event):
    if not event.args:
        event.reply("cfg|cmds|fleet|kernel|ls|pid|tasks|version")
        return
    bot = bl.k.fleet.get_bot(event.orig)
    cmd = event.args[0]
    if cmd == "cfg":
        if len(event.args) == 2:
            config = bl.k.db.last("%s.%s.Cfg" % ("obi", event.args[1].lower()))
            event.reply(config)
        else:
            event.reply(bl.k.cfg)
    elif cmd == "cmds":
        event.reply("|".join(sorted(bl.k.cmds)))
    elif cmd == "fleet":
        try:
            index = int(event.args[1])
            event.reply(bl.k.fleet.bots[index])
            return
        except (ValueError, IndexError):
            event.reply([bl.typ.get_type(x) for x in bl.k.fleet.bots])
    elif cmd == "kernel":
        event.reply(bl.k)
    elif cmd == "ls":
        event.reply("|".join(os.listdir(os.path.join(bl.k.cfg.workdir, "store"))))
    elif cmd == "pid":
        event.reply(str(os.getpid()))
    elif cmd == "tasks":
        psformat = "%-8s %-50s"
        result = []
        for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
            if str(thr).startswith("<_"):
                continue
            d = vars(thr)
            o = bl.obj.Object()
            bl.obj.update(o, d)
            if getattr(o, "sleep", None):
                up = o.sleep - int(time.time() - o.state.latest)
            else:
                up = int(time.time() - bl.k.state.starttime)
            result.append((up, thr.getName(), o))
        nr = -1
        for up, thrname, o in sorted(result, key=lambda x: x[0]):
            nr += 1
            res = "%s %s" % (nr, psformat % (bl.tms.elapsed(up), thrname[:60]))
            if res.strip():
                event.reply(res)
    elif cmd == "uptime":
        event.reply(bl.tms.elapsed(time.time() - bl.k.state.starttime))
    elif cmd == "version":
        res = []
        res.append("BOTLIB %s" % bl.__version__)
        for name, mod in bl.k.table.items():
            if not mod:
                continue
            ver = getattr(mod, "__version__", None)
            if ver:
                txt = "%s %s" % (name, ver)
                res.append(txt.upper())
        if res:
            event.reply(" | ".join(res))
