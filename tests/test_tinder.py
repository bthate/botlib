# BOTLIB - the bot library !
#
#

import random, sys, unittest

from bot.krn import k

ignore = ["ps",]
nrtimes = 1

for x in sys.argv:
    try:
        nrtimes = int(x)
    except ValueError:
        continue

class Test_Tinder(unittest.TestCase):

    def test_all(self):
        for x in range(nrtimes):
            tests(k)

def tests(b):
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        k.cmd(cmd)
        k.cmd(cmd + " " + "arg")