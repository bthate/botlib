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
Description=OKBOT - the 24/7 IRC channel daemon
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/okbotd

[Install]
WantedBy=multi-user.target
"""

def list_files(wd):
    return "|".join([x for x in os.listdir(os.path.join(wd, "store"))])

def hup(event):
    if not root():
        event.reply("you need root permission.")
        return
    for x in os.popen("service okbot stop").readlines():
        print(x.rstrip())
    for x in os.popen("service okbot start").readlines():
        print(x.rstrip())
    for x in os.popen("systemctl status okbot --no-pager").readlines():
        print(x.rstrip())
    event.reply("ok")

def install(event):
    if not root():
        event.reply("you need root permission.")
        return
    f = open("/etc/systemd/system/okbot.service", "w")
    f.write(txt)
    f.close()
    os.popen("systemctl enable okbot")
    os.popen("systemctl daemon-reload")
    event.reply("ok")

def remove(event):
    if not root():
        event.reply("you need root permission.")
        return
    p = "/etc/systemd/system/okbot.service"
    if os.path.exists(p):
        for l in os.popen("rm %s" % p).readlines():
            print(l) 
    event.reply("ok")

def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))

def udp(event):
    if len(sys.argv) > 2:
        txt = " ".join(sys.argv[2:])
        toudp(host, port, txt)
        return
    if not select.select([sys.stdin,],[],[],0.0)[0]:
        return
    while 1:
        try:
            (i, o, e) = select.select([sys.stdin,], [], [sys.stderr,])
        except KeyboardInterrupt:
            return
        if e:
            break
        stop = False
        for sock in i:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            toudp(host, port, txt)
        if stop:
            break
