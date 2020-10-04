# OLIB - object library
#
#

import ol
import os
import time

def fnd(event):
    if not event.args:
        wd = os.path.join(ol.wd, "store", "")
        ol.cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0].split(".")[-1].lower() for x in fns})
        if fns:
            event.reply(",".join(fns))
        return
    k = ol.krn.get_kernel()
    otype = event.args[0]
    otypes = ol.get(k.names, otype, [otype,])
    args = list(ol.keys(event.__prs__.gets))
    try:
        arg = event.args[1:]
    except ValueError:
        arg = []
    args.extend(arg)
    nr = -1
    for otype in otypes:
        for o in ol.dbs.find(otype, event.__prs__.gets, event.__prs__.index, event.__prs__.timed):
            nr += 1
            if "f" in event.__prs__.opts:
                pure = False
            else:
                pure = True
            txt = "%s %s" % (str(nr), ol.format(o, args, pure, event.__prs__.skip))
            if "t" in event.__prs__.opts:
                txt += " %s" % (ol.tms.elapsed(time.time() - ol.tms.fntime(o.__stp__)))
            event.reply(txt)
