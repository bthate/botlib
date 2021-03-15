# This file is placed in the Public Domain.

"test objects"

# imports

import bot
import unittest

# classes

class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = bot.O()
        o.test = "bla"
        v = bot.json(o)
        self.assertEqual(str(o), v)
    