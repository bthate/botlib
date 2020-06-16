# BOTLIB - the bot library !
#
#

from .krn import get_kernel
from .spc import cfg, check, cmd, execute, get_kernel, root

k = get_kernel()

def daemon(event):
    check("bot")
    k.scan("bot")
    k.start()
    k.init("bot.irc,bot.rss")
    k.wait()

def hup(event):
    if not root():
        event.reply("you need root permission.")
        return
    for x in os.popen("service botd stop").readlines():
        print(x.rstrip())
    for x in os.popen("service botd start").readlines():
        print(x.rstrip())
    for x in os.popen("systemctl status botd --no-pager").readlines():
        print(x.rstrip())
    event.reply("ok")

def install(event):
    if not root():
        event.reply("you need root permission.")
        return
    f = open("/etc/systemd/system/botd.service", "w")
    f.write(txt)
    f.close()
    os.popen("systemctl enable botd")
    os.popen("systemctl daemon-reload")
    event.reply("ok")

def remove(event):
    if not root():
        event.reply("you need root permission.")
        return
    p = "/etc/systemd/system/botd.service"
    if os.path.exists(p):
        for l in os.popen("rm %s" % p).readlines():
            print(l) 
    event.reply("ok")

txt="""[Unit]
Description=BOTD - the 24/7 IRC channel daemon
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/botd

[Install]
WantedBy=multi-user.target
"""
