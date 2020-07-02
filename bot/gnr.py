# BOTLIB - the bot library !
#
#

import json, os, sys, _thread

from .obj import cdir, get, get_type, update
from .utl import locked

lock = _thread.allocate_lock()

def edit(o, setter, skip=False):
    try:
        setter = vars(setter)
    except (TypeError, ValueError):
        pass
    if not setter:
        setter = {}
    count = 0
    for key, value in setter.items():
        if skip and value == "":
            continue
        count += 1
        if value in ["True", "true"]:
            o[key] = True
        elif value in ["False", "false"]:
            o[key] = False
        else:
            o[key] = value
    return count

def find(o, val):
    for item in o.values():
        if val in item:
            return True
    return False

def last(o, strip=False):
    from .dbs import Db
    db = Db()
    path, l = db.last_fn(str(get_type(o)))
    if l:
        if strip:
            update(o, strip(l))
        else:
            update(o, l)
        o._path = path

def merge(o, oo, vals=None):
    if vals is None:
        vals = ["",]
    return update(o, strip(oo, vals))

def search(o, match=None):
    res = False
    if match is None:
        return res
    for key, value in match.items():
        val = get(o, key, None)
        if val:
            if not value:
                res = True
                continue
            if value in str(val):
                res = True
                continue
            res = False
            break
    return res

def slc(o, keys=None):
    res = type(o)()
    for k in o:
        if keys is not None and k in keys:
            continue
        res[k] = o[k]
    return res

def strip(o, skip=None):
    for k in o:
        if skip is not None and k in skip:
            continue
        if not k:
            del o[k]
    return o

def tojson(o):
    return json.dumps(o, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

def tostr(o, keys=None):
    if keys is None:
        keys = vars(o).keys()
    res = []
    txt = ""
    for key in keys:
        if key == "stamp":
            continue
        val = get(o, key, None)
        if not val:
            continue
        val = str(val)
        if key == "text":
            val = val.replace("\\n", "\n")
        res.append((key, val))
    for key, val in res:
        txt += "%s=%s%s" % (key, val.strip(), " ")
    return txt.strip()

