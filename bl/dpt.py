# BOTLIB - Framework to program bots.
#
# 

import bl
import logging

def dispatch(handler, event):
    try:
        event.parse()
    except bl.err.ENOTXT:
        event.ready()
        return
    event._func = handler.get_cmd(event.chk)
    if event._func:
        event._calledfrom = str(event._func)
        try:
            event._func(event)
        except Exception as ex:
            logging.error(bl.trc.get_exception())
        event.show()
    event.ready()
