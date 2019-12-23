# BOTLIB - Framework to program bots.
#
# 

import bl

def dispatch(handler, event):
    try:
        event.parse()
    except bl.err.ENOTXT:
        event.ready()
        return
    event._func = handler.get_cmd(event.chk)
    if event._func:
        event._calledfrom = str(event._func)
        event._func(event)
        event.show()
    event.ready()
