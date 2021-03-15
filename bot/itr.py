# This file is placed in the Public Domain.

import ob
import os
import inspect
import pkgutil

def find_cmds(mod):
    cmds = ob.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in cmds:
                    cmds[key] = o
    return cmds

def find_funcs(mod):
    funcs = ob.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in funcs:
                    funcs[key] = "%s.%s" % (o.__module__, o.__name__)
    return funcs

def find_mods(mod):
    mods = ob.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in mods:
                    mods[key] = o.__module__
    return mods

def find_modules(pns):
    mods = []
    for mn in ob.itr.find_all(pns):
        if mn in mods:
            continue
        mod = ob.direct(mn)
        if ob.itr.find_cmds(mod):
            mods.append(mn)
    return mods

def find_classes(mod):
    nms = ob.ObjectList()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            nms.append(o.__name__, t)
    return nms

def find_class(mod):
    mds = ob.ObjectList()
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            mds.append(o.__name__, o.__module__)
    return mds

def find_names(mod):
    tps = ob.Object()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, ob.Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            if t not in tps:
                tps[o.__name__.lower()] = t
    return tps

def find_all(names):
    from . import cfg
    for pn in ob.spl(names):
        try:
            mod = ob.direct(pn)
        except ModuleNotFoundError:
            continue
        if "__file__" in dir(mod) and mod.__file__:
            pths = [os.path.dirname(mod.__file__),]
            for m, n, p in pkgutil.iter_modules(pths):
                fqn = "%s.%s" % (pn, n)
                yield fqn
        else:
            p = list(mod.__path__)[0]
            if not os.path.exists(p):
                continue
            for mn in [x[:-3] for x in os.listdir(p) if x.endswith(".py")]:
                fqn = "%s.%s" % (pn, mn)
                yield fqn

def get_names(pkgs):
    res = ob.Object()
    for pkg in ob.spl(pkgs):
        for mod in mods(pkg):
            n = ob.itr.find_names(mod)
            ob.update(res, n)
    return res

def scan(h, mod):
    mn = mod.__name__
    h.pnames[mn.split(".")[-1]] = mn
    ob.update(h.modnames, find_mods(mod))
    h.names.update(find_names(mod))

def walk(names):
    oo = ob.Object()
    oo.pnames = ob.Object()
    oo.names = ob.ObjectList()
    oo.modnames = ob.Object()
    for mn in find_all(names):
        mod = ob.direct(mn)
        oo.pnames[mn.split(".")[-1]] = mn
        ob.update(oo.modnames, find_mods(mod))
        oo.names.update(find_names(mod))
    return oo
