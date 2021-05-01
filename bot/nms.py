# This file is placed in the Public Domain.

import json as js
import inspect

from obj import Default, Object

class Names(Object):

    inits = Object({
    })

    names = Default({
    })

    modules = Object({
    })

    @staticmethod
    def add(func):
        Names.modules[func.__name__] = func.__module__

    @staticmethod
    def getinit(nm, dft=None):
        return Names.inits.get(nm, dft)

    @staticmethod
    def getnames(nm, dft=None):
        return Names.names.get(nm, dft)

    @staticmethod
    def getmodule(mn):
        return Names.modules.get(mn, None)

    @staticmethod
    def tbl(tbl):
        Names.inits.update(tbl["inits"])
        Names.names.update(tbl["names"])
        Names.modules.update(tbl["modules"])

def findnames(mod):
    tps = Object()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            if t not in tps:
                tps[o.__name__.lower()] = t
    return tps
