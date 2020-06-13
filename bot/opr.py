# OKBOT - the ok bot !
#
#

import ok, os, select, socket, threading, time

from ok.obj import Object, cdir, starttime
from ok.krn import get_kernel
from ok.shl import root
from ok.tms import elapsed

k = get_kernel()

txt="""[Unit]
Description=BOTD - the 24/7 IRC channel daemon
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/botd

[Install]
WantedBy=multi-user.target
"""

def list_files(wd):
    return "|".join([x for x in os.listdir(os.path.join(wd, "store"))])

def meet(event):
    if not event.args:
        event.reply("meet <userhost>")
        return
    origin = event.args[0]
    origin = k.users.userhosts.get(origin, origin)
    k.users.meet(origin, perms)
    event.reply("ok")

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Object()
        o.update(d)
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res:
            event.reply(res.rstrip())

