# OKLIB - the ok library !
#
#

import argparse, logging

from .log import level
from .obj import Default, Object

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

def parse_cli(name, opts=[], usage=None):
    ns = Object()
    make_opts(ns, opts, usage)
    cfg = Default(ns)
    cfg.name = name
    cfg.txt = " ".join(cfg.args)
    if not cfg.workdir:
        cfg.workdir = lo.hd(".%s" % name)
    ok.obj.workdir = cfg.workdir
    cdir(os.path.join(cfg.workdir, "store", ""))
    if cfg.logfile:
        cdir(cfg.logfile)
        touch(cfg.logfile)
    level(cfg.level, cfg.logfile)
    logging.warning("%s %s started on %s" % (cfg.name.upper(), cfg.version, time.ctime(time.time())))
    if cfg.logfile:
        logging.warning("logging.is in %s" % cfg.logfile)
    return cfg

def rlog(level, txt, extra):
    logging.log(level, "%s %s" % (txt, extra))



