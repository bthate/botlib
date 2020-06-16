# BOTLIB - the bot library !
#
#

from ok.krn import get_kernel
from bot.spc import cfg, check, cmd, execute, get_kernel, root

def daemon(event):
    check("bot")
    k = get_kernel()
    k.scan("bot")
    k.start()
    k.init("bot.irc,bot.rss")
    k.wait()


k = get_kernel()

txt="""[Unit]
Description=BOTLIB - the 24/7 IRC channel daemon
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/botd

[Install]
WantedBy=multi-user.target
"""

def hup(event):
    if not root():
        event.reply("you need root permission.")
        return
    for x in os.popen("service botlib stop").readlines():
        print(x.rstrip())
    for x in os.popen("service botlib start").readlines():
        print(x.rstrip())
    for x in os.popen("systemctl status botlib --no-pager").readlines():
        print(x.rstrip())
    event.reply("ok")

def install(event):
    if not root():
        event.reply("you need root permission.")
        return
    f = open("/etc/systemd/system/okbot.service", "w")
    f.write(txt)
    f.close()
    os.popen("systemctl enable botlib")
    os.popen("systemctl daemon-reload")
    event.reply("ok")

def remove(event):
    if not root():
        event.reply("you need root permission.")
        return
    p = "/etc/systemd/system/botlib.service"
    if os.path.exists(p):
        for l in os.popen("rm %s" % p).readlines():
            print(l) 
    event.reply("ok")

def main():
    check("botlib")
    if root():
        k.cmds.register("hup", hup)
        k.cmds.register("install", install)
        k.cmds.register("remove", remove)
    k.scan("bot")
    cmd(cfg.txt)
       
execute(main)
