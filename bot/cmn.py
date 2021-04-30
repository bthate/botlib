# This file is placed in the Public Domain.

import getpass
import os
import pwd

def locked(l):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockedfunc.__wrapped__ = func
        return lockedfunc
    return lockeddec

def mods(name):
    res = []
    if os.path.exists(name):
        for p in os.listdir(name):
            if p.startswith("__"):
                continue
            if p.endswith(".py"):
                res.append(p[:-3])
    return ",".join(res)

def privileges(name=None):
    if os.getuid() != 0:
        return
    if name is None:
        try:
            name = getpass.getuser()
        except KeyError:
            pass
    try:
        pwnam = pwd.getpwnam(name)
    except KeyError:
        return False
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    old_umask = os.umask(0o22)
    return True

def root():
    if os.geteuid() != 0:
        return False
    return True

def spl(txt):
    return [x for x in txt.split(",") if x]
