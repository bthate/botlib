# BOTLIB - the bot library !
#
#

from .utl import elapsed, fntime

def display(o, txt="", keys=None, options="t", post="", strict=False):
    if not keys:
        keys = list(o.keys())
    txt = txt[:]
    txt += " %s" % format(o, keys, strict=strict) 
    if "t" in options:
       txt += " %s" % elapsed(time.time() - fntime(o._path))
    if post:
       txt += " " + post
    return txt.strip()

def format(o, keys=None, strict=False):
    if keys is None:
        keys = list(vars(o).keys())
    res = []
    txt = ""
    for key in keys:
        val = o.get(key)
        if not val:
            continue
        val = str(val)
        if key == "text":
            val = val.replace("\\n", "\n")
        res.append((key, val))
    for key, val in res:
        if strict:
            txt += "%s%s" % (val.strip(), " ")
        else:
            txt += "%s=%s%s" % (key, val.strip(), " ")
    return txt.strip()
