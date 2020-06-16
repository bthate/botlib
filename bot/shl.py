# BOTLIB - the bot library !
#
#

import atexit, argparse, logging, os, readline, sys, termios, time, _thread

from .obj import Default, Object
from .krn import get_kernel
from .utl import check, cdir, level

cmds = []
cfg = Object()
logfiled = ""
resume = {}
HISTFILE = ""

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

def parse_cli(name, opts=[], wd="", debug=""):
    import bot.obj
    k = get_kernel()
    ns = Object()
    make_opts(ns, opts)
    k.cfg = Default(ns)
    k.cfg.debug = debug
    k.cfg.name = name
    k.cfg.txt = " ".join(k.cfg.args)
    bot.obj.workdir = k.cfg.workdir = wd or k.cfg.workdir
    cdir(os.path.join(k.cfg.workdir, "store", ""))
    if k.cfg.debug:
        import bot.rss
        bot.rss.debug = True
    level(k.cfg.level)
    logging.warning("%s %s started on %s" % (k.cfg.name.upper(), k.cfg.version, time.ctime(time.time())))
    return k.cfg

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
