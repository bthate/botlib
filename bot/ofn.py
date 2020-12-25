# BOTLIB - ofn.py
#
# this file is placed in the public domain

"object functions (ofn)"

# imports

import datetime
import json
import os
import types
import uuid

# functions

def default(o):
    "return strinfified version of an object"
    from bot.obj import Object
    if isinstance(o, Object):
        return vars(o)
    if isinstance(o, dict):
        return o.items()
    if isinstance(o, list):
        return iter(o)
    if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
        return o
    return repr(o)

def edit(o, setter, skip=False):
    "update an object from a dict"
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

def format(o, keys=None, skip=None):
    "return 1 line output string"
    if keys is None:
        keys = vars(o).keys()
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in keys:
        if key in skip:
            continue
        try:
            val = o[key]
        except KeyError:
            continue
        if not val:
            continue
        val = str(val).strip()
        res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()

def get_name(o):
    "return fully qualified name of an object"
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

def get_type(o):
    "return type of an object"
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def mkstamp(o):
    "create a type/uuid/time stamp"
    timestamp = str(datetime.datetime.now()).split()
    return os.path.join(get_type(o), str(uuid.uuid4()), os.sep.join(timestamp))

def ojson(o, *args, **kwargs):
    "return jsonified string"
    return json.dumps(o, default=default, *args, **kwargs)

def scan(o, txt):
    from bot.obj import items
    for _k, v in items(o):
        if txt in str(v):
            return True
    return False

def search(o, s):
    "search object for a key,value to match dict"
    from bot.obj import get, items
    ok = False
    for k, v in items(s):
        vv = get(o, k)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok

def xdir(o, skip=None):
    "return a dir(o) with keys skipped"
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
 