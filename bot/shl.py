# BOTLIB - the bot library !
#
#

import atexit, argparse, logging, os, readline, sys, termios, time, _thread

from .obj import Default, Object, cdir

cmds = []
cfg = Object()
logfile = ""
resume = {}
HISTFILE = ""

def bexec(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")

def close_history():
    global HISTFILE
    if bot.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bot.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            cdir(HISTFILE)
            touch(HISTFILE)
        readline.write_history_file(HISTFILE)

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def enable_history():
    assert bot.obj.workdir
    HISTFILE = os.path.abspath(os.path.join(bot.obj.workdir, "history"))
    if not os.path.exists(HISTFILE):
        cdir(HISTFILE)
        touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

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

def make_opts(ns, options, usage="", **kwargs):
    kwargs["usage"] = usage
    kwargs["allow_abbrev"] = False
    kwargs["argument_default"] = argparse.SUPPRESS
    kwargs["formatter_class"] = argparse.HelpFormatter
    parser = argparse.ArgumentParser(**kwargs)
    for opt in options:
        if not opt:
            continue
        try:
            parser.add_argument(opt[0], opt[1], action=opt[2], type=opt[3], default=opt[4], help=opt[5], dest=opt[6], const=opt[4], nargs="?")
        except Exception as ex:
            try:
                parser.add_argument(opt[0], opt[1], action=opt[2], default=opt[3], help=opt[4], dest=opt[5])
            except Exception as ex:
                pass
    parser.add_argument('args', nargs='*')
    parser.parse_known_args(namespace=ns)

def parse_cli(name):
    ns = Default()
    if len(sys.argv) <= 1:
        return ns
    ns.name = name
    ns.txt = " ".join(sys.argv[1:])
    ns.update(Options(ns.txt))
    return ns
    
def parse_cli2(name, opts=[], version="", wd=""):
    import bot.obj
    ns = Object()
    make_opts(ns, opts)
    cfg = Default(ns)
    cfg.name = name
    if cfg.args:
        cfg.txt = " ".join(cfg.args)
    if version:
        cfg.version = version
    bot.obj.workdir = cfg.workdir = cfg.workdir or wd or os.path.expanduser("~/.bot")
    if cfg.options:
        for opt in cfg.options.split(","):
            try:
                cfg.index = int(opt)
            except ValueError:
                continue
    level(cfg.level)
    cdir(os.path.join(bot.obj.workdir, "store", ""))
    return cfg

def setcompleter(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
        
def setup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
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
