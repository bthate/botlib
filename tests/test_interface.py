# BOTLIB - the bot library !
#
#

import unittest
import bot.cls

from bot.utl import get_cls

class Test_Interface(unittest.TestCase):

    def test_iface(self):
        for name in dir(bot.cls):
             
            c = get_cls(name)
            