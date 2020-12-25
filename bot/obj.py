# BOTLIB - obj.py
#
# this file is placed in the public domain

"object base class (obj)"

# imports

import datetime
import importlib
import json
import os
import random
import sys
import time
import types
import uuid

from bot.ofn import default, get_type
from bot.utl import cdir, hooked

# defines

wd = ""

# exceptions

class ENOFILENAME(Exception):

    "provided argument is not a filename"

class ENOCLASS(Exception):

    "class is not available"

# classes

class O:

    "basic object"

    __slots__ = ("__dict__",)

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.__dict__.update(args[0])

    def __call__(self):
        pass

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        return self.__dict__.get(k, d)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return json.dumps(self, default=default, sort_keys=True)

class Object(O):

    __slots__ = ("__id__", "__type__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id__ = str(uuid.uuid4())
        self.__type__ = get_type(self)

class Default(Object):

    "uses default values"

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            return super().__getitem__(k, "")

class Cfg(Default):

    "base config class"

class Ol(Object):

    "object list"

    def append(self, key, value):
        "add to list at self[key]"
        if key not in self:
            self[key] = []
        if isinstance(value, type(list)):
            self[key].extend(value)
        else:
            if value not in self[key]:
                self[key].append(value)

    def update(self, d):
        "update from other object list"
        for k, v in d.items():
            self.append(k, v)

# methods

def get(o, k, d=None):
    "return o[k]"
    try:
        res = o.get(k, d)
    except (TypeError, AttributeError):
        res = o.__dict__.get(k, d)
    return res

def items(o):
    "return items (k,v) of an object"
    try:
        return o.items()
    except (TypeError, AttributeError):
        return o.__dict__.items()

def keys(o):
    "return keys of an object"
    try:
        return o.keys()
    except (TypeError, AttributeError):
        return o.__dict__.keys()

def load(o, path):
    "load from disk into an object"
    assert path
    if path.count(os.sep) != 3:
        raise ENOFILENAME(path)
    spl = path.split(os.sep)
    stp = os.sep.join(spl[-4:])
    lpath = os.path.join(wd, "store", stp)
    typ = spl[0]
    id = spl[1]
    with open(lpath, "r") as ofile:
        try:
            v = json.load(ofile, object_hook=hooked)
        except json.decoder.JSONDecodeError as ex:
            return
        if v:
            update(o, v)
    o.__id__ = id
    o.__type__ = typ
    return stp

def register(o, k, v):
    "register key/value"
    o[k] = v

def save(o, stime=None):
    "save object to disk"
    assert wd
    if stime:
        stp = os.path.join(o.__type__, o.__id__,
                           stime + "." + str(random.randint(0, 100000)))
    else:
        timestamp = str(datetime.datetime.now()).split()
        stp = os.path.join(o.__type__, o.__id__, os.sep.join(timestamp))
    opath = os.path.join(wd, "store", stp)
    cdir(opath)
    with open(opath, "w") as ofile:
        json.dump(o, ofile, default=default)
    os.chmod(opath, 0o444)
    return stp

def set(o, k, v):
    "set o[k]=v"
    setattr(o, k, v)

def update(o, d):
    "update object with other object"
    return o.__dict__.update(vars(d))

def values(o):
    "return values of an object"
    try:
        return o.values()
    except (TypeError, AttributeError):
        return o.__dict__.values()
