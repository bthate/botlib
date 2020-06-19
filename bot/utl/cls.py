# BOTLIB - the bot library !
#
#

from .clk import Repeater
from .csl import Console
from .evt import Event
from .flt import Fleet
from .hdl import Handler
from .irc import IRC, DCC
from .krn import Kernel
from .obj import Cfg, Default, DoL, List, Object
from .prs import Parsed
from .rss import Feed, Fetcher
from .thr import Launcher, Thr 
from .udp import UDP
from .usr import User, Users

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
