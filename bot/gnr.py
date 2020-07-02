# BOTLIB - the bot library !
#
#

import json, os, _thread

from .utl import locked

lock = _thread.allocate_lock()

def get(o, k, d=None):
    return o.__dict__.get(k, d)

def items(o):
    return o.__dict__.items()

def keys(o):
    return o.__dict__.keys()

def register(o, k, v):
    os.__dict__[k] = v

def set(o, k, v):
    o.__dict__[k] = v

def update(o, d):
    try:
        return o.__dict__.update(vars(d))
    except (TypeError, ValueError):
        return o.__dict__.update(d)

def values(o):
    return o.__dict__.values()

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

def get_type(o):
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

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

@locked(lock)
def load(o, path, force=False):
    assert path
    import bot.obj
    assert bot.obj.workdir
    lpath = os.path.join(bot.obj.workdir, "store", path)
    if not os.path.exists(lpath):
        cdir(lpath)
    o._path = path
    with open(lpath, "r") as ofile:
        val = json.load(ofile, cls=ObjectDecoder)
        if val:
            update(o, val)

def merge(o, oo, vals=None):
    if vals is None:
        vals = ["",]
    return update(o, strip(oo, vals))


@locked(lock)
def save(o, stime=None):
    import bot.obj
    assert bot.obj.workdir
    if stime:
        o._path = os.path.join(get_type(o), stime) + "." + str(random.randint(1, 100000))
    opath = os.path.join(bot.obj.workdir, "store", o._path)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(stamp(o), ofile, cls=ObjectEncoder, indent=4, skipkeys=True, sort_keys=True)
    return o._path

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

def stamp(o):
    for k in xdir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

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

def xdir(o, skip=None):
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
