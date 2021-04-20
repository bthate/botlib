from bot.evt import Event

def rec(event):
    event.say("reconnect")
    bot = event.bot()
    bot.reconnect()
    bot.connected.wait()
    event.say("done")

def rse(event):
    raise ConnectionResetError

def rse2(event):
    e = botl.evt.Event()
    e.cmd = "raise"
    b = event.bot()
    b.put(e)
