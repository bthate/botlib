# BOTLIB - the bot library !
#
#

""" objects to save to disk. """

from .obj import Object
from .pst import names
from .utl import hook, search

## classes

class Db(Object):

    """ database interface to Objects stored on disk. """

    def all(self, otype, selector=None, index=None, delta=None):
        """ return all objects of a type. """
        nr = -1
        if selector is None:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield o

    def deleted(self, otype):
        """ show all deleted records of a type. """
        nr = -1
        for fn in names(otype):
            o = hook(fn)
            nr += 1
            if "_deleted" not in o or not o._deleted:
                continue
            yield o

    def find(self, otype, selector=None, index=None, delta=0):
        """ find all objects of a type matching fields in the provided selector. """
        nr = -1
        if selector is None:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            if search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def find_value(self, otype, value, index=None, delta=0):
        """ find object that have values that matches provided string. """
        nr = -1
        for fn in names(otype, delta):
            o = hook(fn)
            if o.find(value):
                nr += 1
                if index is not None and nr != index:
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                yield o

    def last(self, otype):
        """ return last saved object of a type. """
        fns = names(otype)
        if fns:
            fn = fns[-1]
            return hook(fn)

    def last_fn(self, otype):
        """ return filename of last saved object of a type. """
        fns = names(otype)
        if fns:
            fn = fns[-1]
            return (fn, hook(fn))
        return (None, None)

    def last_all(self, otype, selector=None):
        """ return the last object of a type matching the selector. """
        nr = -1
        res = []
        if not selector:
            selector = {}
        for fn in names(otype, delta):
            o = hook(fn)
            if selector is not None and search(o, selector):
                nr += 1
                if index is not None and nr != index:
                    continue
                res.append((fn, o))
            else:
                res.append((fn, o))
        if res:
            s = sorted(res, key=lambda x: fntime(x[0]))
            if s:
                return s[-1][-1]
        return None
