# BOTLIB - the bot library !
#
#

import logging

from .obj import Object, cdir
from .shl import touch

format = Object()
format.large = "%(asctime)-8s %(module)10s.%(lineno)-4s %(message)-50s (%(threadName)s)"
format.source = "%(asctime)-8s %(message)-50s (%(module)s.%(lineno)s)"
format.time = "%(asctime)-8s %(message)-72s"
format.log = "%(message)s"
format.super = "%(asctime)-8s -=- %(message)-50s -=- (%(module)s.%(lineno)s)" 
format.normal = "%(asctime)-8s -=- %(message)-60s"
format.plain = "%(message)-0s"

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }

def level(loglevel, logfile="", nostream=False):
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
            logging.warning("wrong level %s" % loglevel)
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
