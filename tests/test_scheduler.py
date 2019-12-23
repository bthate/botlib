# BOTLIB - Framework to program bots
#
# 

from bl.event import Event
from bl.space import cfg, kernel, template

import unittest

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = Event()
        e.origin = "root@shell"
        e.txt = "version"
        kernel.put(e)
        e.wait()
        self.assertTrue("BOTLIB" in e._result[0])
