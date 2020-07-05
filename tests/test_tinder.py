# BOTLIB - the bot library !
#
#

import random, sys, unittest

from bot.krn import k

ignore = ["ps",]

class Test_Tinder(unittest.TestCase):

    def test_all(self):
        for x in range(k.cfg.index or 1):
            tests(k)

def tests(b):
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        k.cmd(cmd + " " + "arg")
