# BOTLIB - the bot library !
#
#

""" objects to save to disk. """

import importlib, os, sys, time

from .err import ENOFILENAME

## utilities

def cdir(path):
    """ create directory. """
    if os.path.exists(path):
        return
    res = ""
    path2, fn = os.path.split(path)
    for p in path2.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass
    return True

def fntime(daystr):
    """ return time from filename. """
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    try:
        datestr, rest = datestr.rsplit(".", 1)
    except ValueError:
        rest = ""
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            t += float("." + rest)
    except ValueError:
        t = 0
    return t

def get_cls(name):
    """ return class by full qualified name. """
    from .err import ENOCLASS
    try:
        modname, clsname = name.rsplit(".", 1)
    except:
        raise ENOCLASS(name)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_type(o):
    """ return type of an object. """
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def hook(fn):
    """ return object from filename. """
    from bot.obj import load
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILENAME(fn)
    o = get_cls(t)()
    load(o, fn)
    return o

def hooked(d):
    """ convert to object depending on filename stamp. """
    from .obj import update
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        update(o, d)
        return o
    return d

def locked(l):
    """ lock on provided lock. """
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockedfunc.__doc__ = func.__doc__
        return lockedfunc
    return lockeddec

def xdir(o, skip=None):
    """ return dir() but skipping unwanted keys. """
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
