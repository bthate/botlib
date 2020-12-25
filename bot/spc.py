# BOTLIB - spc.py
#
# this file is placed in the public domain

"runtime objects"

# imports

from bot.hdl import Bus, Handler, cmd
from bot.rss import Fetcher
from bot.trm import termsave, termreset

# defines

def __dir__():
    return ("bus", "fetcher", "h")

# functions

def execute(main):
    "provide context for funcion"
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except Exception as ex:
        print(get_exception())
    finally:
        termreset()

# runtime

bus = Bus()
fetcher = Fetcher()
h = Handler()
h.register("cmd", cmd)
