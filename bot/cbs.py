# BOTLIB - the bot library !
#
#

def error(handler, event):
    handler.state.nrerror += 1
    print(event._error)
    handler.state.error = event._error
    handler._connected.clear()
    handler.stop()
    if handler.state.nrerror < 3:
        launch(init, k)

def ERROR(handler, event):
    handler.error = event.error

def NOTICE(handler, event):
    if event.txt.startswith("VERSION"):
        txt = "\001VERSION %s %s - %s\001" % (cfg.name or "OKBOT", "1", "the ok bot !")
        handler.command("NOTICE", event.channel, txt)

def PRIVMSG(handler, event):
    if event.txt.startswith("DCC CHAT"):
        if k.cfg.owner and not k.users.allowed(event.origin, "USER"):
            return
        try:
            dcc = DCC()
            dcc.cmds.update(handler.cmds)
            dcc.encoding = "utf-8"
            print(dcc)
            launch(dcc.connect, event)
            return
        except ConnectionError:
            return
    if event.txt and event.txt[0] == handler.cc:
        if k.cfg.owner and not k.users.allowed(event.origin, "USER"):
            return
        e = Command(event.txt[1:], event.orig, event.origin, event.channel)
        dispatch(handler, e)

def QUIT(handler, event):
    if handler.cfg.server in event.orig:
        handler.stop()
        launch(init, event)
