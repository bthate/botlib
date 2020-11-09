"edit objects"

import obj

from dbs import lasttype, list_files
from obj import get, get_cls, save
from ofn import edit

def edt(event):
    "edit objects"
    if not event.args:
        return event.reply(" | ".join(list_files(obj.wd)))
    cn = event.args[0]
    l = lasttype(cn)
    if not l:
        return
    if not event.prs.sets:
        event.reply(l)
        return
    edit(l, event.prs.sets)
    save(l)
    event.reply("ok")
