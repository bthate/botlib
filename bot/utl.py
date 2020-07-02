# BOTLIB - the bot library !
#
#

import os, _thread

lock = _thread.allocate_lock()

def bexec(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")

def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def drop():
    ruid = pwd.getpwnam("botd")[2]
    os.setuid(ruid)
    os.umask(0o007)

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
        return lockedfunc
    return lockeddec

def names(name, delta=None):
    if not name:
        return []
    p = os.path.join(workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if delta:
        past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

def fntime(daystr):
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
    try:
        modname, clsname = name.rsplit(".", 1)
    except:
        raise ENOCLASS(name)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    load(o, fn)
    return o

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        o.update(d)
        return o
    return d

def list_files(wd):
    return "|".join(os.path.join(wd, "store"))

def root():
    if os.geteuid() != 0:
        return False
    return True

def setwd(name):
    if root():
        bot.obj.workdir = "/var/lib/%s" % name
    else:
        bot.obj.workdir = os.path.expanduser("~/.%s" % name)

def spl(txt):
    return iter([x for x in txt.split(",") if x])

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def writepid():
    assert bot.obj.workdir
    path = os.path.join(bot.obj.workdir, "pid")
    if not os.path.exists(path):
        cdir(path)
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
