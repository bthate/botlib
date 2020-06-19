# BOTLIB - the bot library !
#
#

import unittest
import bot.all

from bot.obj import get_cls

class Test_Interface(unittest.TestCase):

    def test_iface(self):
        for name in dir(bot.all):
            c = get_cls(name)
            