# BOTLIB - the bot library !
#
#

import datetime, logging, logging.handlers, importlib, os, string, sys, time, types, traceback

format = {}
format["large"] = "%(asctime)-8s %(module)10s.%(lineno)-4s %(message)-50s (%(threadName)s)"
format["source"] = "%(asctime)-8s %(message)-50s (%(module)s.%(lineno)s)"
format["time"] = "%(asctime)-8s %(message)-72s"
format["log"] = "%(message)s"
format["super"] = "%(asctime)-8s -=- %(message)-50s -=- (%(module)s.%(lineno)s)" 
format["normal"] = "%(asctime)-8s -=- %(message)-60s"
format["plain"] = "%(message)-0s"

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }

logfile = ""

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
   "%d, %b %Y %H:%M:%S +0000"
]

year_formats = [
    "%b %H:%M",
    "%b %H:%M:%S",
    "%a %H:%M %Y",
    "%a %H:%M",
    "%a %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m %H:%M:%S",
    "%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%d-%m %H:%M",
    "%m-%d %H:%M",
    "%H:%M:%S",
    "%H:%M"
]

allowedchars = string.ascii_letters + string.digits + '_+/$.-'

## execute

def bexec(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")

def direct(name):
    return importlib.import_module(name)

## filesystem

def cdir(path):
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

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass

def root():
    if os.geteuid() != 0:
        return False
    return True

## exceptions

def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        if fname.endswith(".py"):
            plugfile = fname[:-3].split(os.sep)
        else:
            plugfile = fname.split(os.sep)
        mod = []
        for element in plugfile[::-1]:
            mod.append(element)
            if "ok" in element:
                break
        ownname = ".".join(mod[::-1])
        result.append("%s:%s" % (ownname, linenr))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

## time related

def day():
    return str(datetime.datetime.today()).split()[0]

def days(path):
    return elapsed(time.time() - fntime(path))

def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    elif sec < 1 or not short:
        txt += "%.3fs" % sec
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def get_time(daystr):
    for f in year_formats:
        try:
            t = time.mktime(time.strptime(daystr, f))
            return t
        except Exception:
            pass

def now():
    return str(datetime.datetime.now()).split()[0]

def parse_date(daystr):
    if daystr.startswith("-"):
        neg = True
        daystr = daystr[1:]
    else:
        neg = False
    val = 0
    total = 0
    for c in daystr:
        if c not in ["s", "m", "h", "d", "w", "y"]:
            try:
                val = int(c)
            except ValueError:
                pass
            continue
        if c == "y":
            total += val * 3600*24*365
        if c == "w":
            total += val * 3600*24*7
        elif c == "d":
            total += val * 3600*24
        elif c == "h":
            total += val * 3600
        elif c == "m":
            total += val * 60
        else:
            total += val
        val = 0
    if neg:
        return 0 - total
    else:
        return total 

def rtime():
    res = str(datetime.datetime.now()).replace(" ", os.sep)
    return res

def today():
    return datetime.datetime.today().timestamp()

def to_day(daystring):
    line = ""
    daystr = str(daystring)
    for word in daystr.split():
        if "-" in word:
            line += word + " "
        elif ":" in word:
            line += word
    if "-" not in line:
        line = day() + " " + line
    try:
        return get_time(line.strip())
    except ValueError:
        pass

def to_time(daystr):
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
            break
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    return res

## names

def get_name(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

## udp

def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))

def list_files(wd):
    return "|".join([x for x in os.listdir(os.path.join(wd, "store"))])

## logging

def level(loglevel, nostream=False):
    if not loglevel:
        loglevel = "error"
    if logfile and not os.path.exists(logfile):
        cdir(logfile)
        touch(logfile)
    datefmt = '%H:%M:%S'
    format_time = "%(asctime)-8s %(message)-70s"
    format_plain = "%(message)-0s"
    loglevel = loglevel.upper()
    logger = logging.getLogger("")
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    try:
        logger.setLevel(loglevel)
    except ValueError:
        pass
    formatter = logging.Formatter(format_plain, datefmt)
    if nostream:
        dhandler = DumpHandler()
        dhandler.propagate = False
        dhandler.setLevel(loglevel)
        logger.addHandler(dhandler)
    else:
        handler = logging.StreamHandler()
        handler.propagate = False
        handler.setFormatter(formatter)
        try:
            handler.setLevel(loglevel)
            logger.addHandler(handler)
        except ValueError:
            loglevel = "ERROR"
    if logfile:
        formatter2 = logging.Formatter(format_time, datefmt)
        filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
        filehandler.propagate = False
        filehandler.setFormatter(formatter2)
        try:
            filehandler.setLevel(loglevel)
        except ValueError:
            pass
        logger.addHandler(filehandler)
    return logger

def rlog(level, txt):
    logging.log(LEVELS.get(level, "error"), txt)

## types

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

def get_type(o):
    t = type(o)
    if t == type:
        try:
            return "%s.%s" % (o.__module__, o.__name__)
        except AttributeError:
            pass
    return str(type(o)).split()[-1][1:-2]

def hook(fn):
    t = fn.split(os.sep)[0]
    if not t:
        t = fn.split(os.sep)[0][1:]
    if not t:
        raise ENOFILE(fn)
    o = get_cls(t)()
    o.load(fn)
    return o

def hooked(d):
    if "stamp" in d:
        t = d["stamp"].split(os.sep)[0]
        o = get_cls(t)()
        o.update(d)
        return o

def stamp(o):
    from .obj import Object
    for k in dir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

## string

def strip(o, vals=["",]):
    rip = []
    for k in o:
        value = o.get(k, None)
        for v in vals:
            if value == v:
                rip.append(k)
    for k in rip:
        del o[k]
    return o
