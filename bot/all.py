# This file is placed in the Public Domain

"all modules"

from botl.krn import Kernel

import botl.cms
import botl.hdl
import botl.irc
import botl.krn
import botl.obj

Kernel.addmod(botl.cms)
Kernel.addmod(botl.hdl)
Kernel.addmod(botl.irc)
Kernel.addmod(botl.krn)
Kernel.addmod(botl.obj)
