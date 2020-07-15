# BOTLIB - the bot library !
#
#

""" objects to save to disk. """

import datetime, json, os, time

from .utl import get_type, hooked

## classes

class Object:

    """ base Object to inherit from, provides a __stamp__ hidden attribute to load/save from. """

    __slots__ = ("__dict__", "__stamp__")

    def __init__(self):
        """ create object and set __stamp__. """
        self.__stamp__ = os.path.join(get_type(self), str(datetime.datetime.now()).replace(" ", os.sep))

    def __delitem__(self, k):
        """ remove item. """
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        """ return item, use None as default. """
        return self.__dict__.get(k, d)

    def __iter__(self):
        """ iterate over the keys. """
        return iter(self.__dict__.keys())

    def __len__(self):
        """ determine length of this object. """
        return len(self.__dict__)

    def __lt__(self, o):
        """ check for lesser than. """
        return len(self) < len(o)

    def __setitem__(self, k, v):
        """ set item to value and return reference to it. """
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        """ return a 4 space indented json string. """
        return json.dumps(self, cls=ObjectEncoder)

class ObjectEncoder(json.JSONEncoder):

    """ encode an Object to string. """

    def default(self, o):
        """ return string for object. """
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        return repr(o)

class ObjectDecoder(json.JSONDecoder):

    """ decode an Object from string. """

    def decode(self, o):
        """ return object from string. """
        return json.loads(o, object_hook=hooked)
