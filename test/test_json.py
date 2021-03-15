# This file is placed in the Public Domain.

"test objects"

# imports

import ob
import unittest

# classes

class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = ob.O()
        o.test = "bla"
        v = ob.json(o)
        self.assertEqual(str(o), v)
    