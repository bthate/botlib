# BOTLIB - the bot library
#
#

import types, unittest

from bot.obj import Object

class Test_Object(unittest.TestCase):

    def test_empty(self):
        o = Object()
        self.assertTrue(not o) 

    def test_final(self):
        with self.assertRaises(TypeError):
            o = Object()
            o.last = "bla"
            o.last()
