# BOTLIB - Framework to program bots
#
# 

from botlib.event import Event
from botlib.space import cfg, kernel, template

import unittest

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = Event()
        e.origin = "root@shell"
        e.txt = "version"
        kernel.put(e)
        e.wait()
        self.assertTrue("BOTLIB" in e._result[0])
