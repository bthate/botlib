# BOTLIB - the bot library !
#
#

from .krn import get_kernel

k = get_kernel()

def dispatch(handler, event):
    func = k.cmds.get(event.cmd, None)
    if func:
        try:
            func(event)
        except Exception as ex:
            print(get_exception())
            return
    event.show()
    event.ready()

def ERROR(handler, event):
    handler.state.nrerror += 1
    handler.state.error = event._error
    handler._connected.clear()
    handler.stop()
    if handler.state.nrerror < 3:
        handler.start()

def NOTICE(handler, event):
    if event.txt.startswith("VERSION"):
        txt = "\001VERSION %s %s - %s\001" % (cfg.name or "OKBOT", "1", "the ok bot !")
        handler.command("NOTICE", event.channel, txt)

def PRIVMSG(handler, event):
    if event.txt.startswith("DCC CHAT"):
        if k.cfg.owner and not k.users.allowed(event.origin, "USER"):
            return
        try:
            from .irc import DCC
            dcc = DCC()
            dcc.cmds.update(handler.cmds)
            dcc.encoding = "utf-8"
            k.launch(dcc.connect, event)
            return
        except ConnectionError:
            return
    if event.txt and event.txt[0] == handler.cc:
        if k.cfg.owner and not k.users.allowed(event.origin, "USER"):
            return
        e = Command(event.txt[1:], event.orig, event.origin, event.channel)
        k.dispatch(handler, e)

def QUIT(handler, event):
    if handler.cfg.server in event.orig:
        handler.stop()
