# This file is placed in the Public Domain

"all modules"

from bot.krn import Kernel

import bot.cms
import bot.fnd
import bot.hdl
import bot.irc
import bot.krn
import bot.obj

Kernel.addmod(bot.cms)
Kernel.addmod(bot.fnd)
Kernel.addmod(bot.hdl)
Kernel.addmod(bot.irc)
Kernel.addmod(bot.krn)
Kernel.addmod(bot.obj)
