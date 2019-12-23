# BOTLIB - Framework to program bots.
#
# 

import argparse
import atexit
import logging
import optparse
import os
import readline
import time
import bl
import bl.log

cmds = []

from bl.trc import get_exception 
from bl.trm import reset, save

HISTFILE = ""

def __dir__():
    return ("daemon", "execute", "parse_cli", "set_completer")

def close_history():
    global HISTFILE
    assert bl.workdir
    if not HISTFILE:
        HISTFILE = os.path.join(bl.workdir, "history")
    if not os.path.isfile(HISTFILE):
        bl.utl.cdir(HISTFILE)
        bl.utl.touch(HISTFILE)
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

def enable_history():
    global HISTFILE
    assert bl.workdir
    HISTFILE = os.path.abspath(os.path.join(bl.workdir, "history"))
    if not os.path.exists(HISTFILE):
        bl.utl.touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    save()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except Exception:
        logging.error(get_exception())
    reset()
    close_history()

def get_completer():
    return readline.get_completer()

def make_opts(ns, options, **kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    for opt in options:
        if not opt:
            continue
        if opt[2] == "store":
            parser.add_argument(opt[0], opt[1], action=opt[2], type=opt[3], help=opt[4], dest=opt[5])
        else:
            parser.add_argument(opt[0], opt[1], action=opt[2], default=opt[3], help=opt[4], dest=opt[5])
    parser.add_argument('args', nargs='*')
    parser.parse_known_args(namespace=ns)
  
def parse_cli(name="blbot", version=None, opts=[], wd=None, level="error"):
    cfg = bl.cfg.Cfg()
    make_opts(cfg, opts)
    cfg.debug = False
    cfg.name = name
    cfg.version = version
    cfg.workdir = cfg.workdir or wd or bl.utl.hd(".%s" % cfg.name)
    cfg.logdir = cfg.logdir or os.path.join(cfg.workdir, "logs")
    cfg.options = ""
    cfg.owner = ""
    cfg.txt = " ".join(cfg.args)
    sp = os.path.join(cfg.workdir, "store") + os.sep
    if not os.path.exists(sp):
        bl.utl.cdir(sp)
    bl.workdir = cfg.workdir
    bl.log.level(cfg.level or level, cfg.logdir)
    bl.obj.update(bl.k.cfg, cfg, [], False)
    logging.warning("%s started (%s) at %s" % (cfg.name.upper(), cfg.level or level, time.ctime(time.time())))
    logging.warning("logging at %s" % bl.log.logfiled)
    return bl.k.cfg

def set_completer(commands):
    global cmds
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def writepid():
    path = os.path.join(bl.k.cfg.workdir, "blbot.pid")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
