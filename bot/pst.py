# BOTLIB - the bot library
#
#

""" objects to save to disk. """

from .obj import Object, ObjectDecoder, ObjectEncoder, os, time, json
from .utl import cdir, fntime, stamp

## defines

workdir = None

## defines

def names(name, delta=None):
    """ return filenames in the working directory. """
    if not name:
        return []
    assert workdir
    p = os.path.join(workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if not delta:
        delta = 0
    past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

## classes

class Persist(Object):

    """ provide load and save to json files. """

    def load(self, path, force=False):
        """ load an object from json file at the provided path. """
        assert path
        assert workdir
        self.__stamp__ = path
        lpath = os.path.join(workdir, "store", path)
        cdir(lpath)
        with open(lpath, "r") as ofile:
            val = json.load(ofile, cls=ObjectDecoder)
            if val:
                if isinstance(val, Object):
                    self.__dict__.update(vars(val))
                else:
                    self.__dict__.update(val)

    def save(self, stime=None):
        """ save this object to a json file, uses the hidden attribute __stamp__. """
        assert workdir
        if stime:
            self.__stamp__ = os.path.join(get_type(self), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self.__stamp__)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder)
        return self.__stamp__

