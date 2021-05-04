# This file is placed in the Public Domain.

import unittest

from edt import edit
from obj import Cfg
from prs import parse_txt
from run import kernel

cfg = Cfg()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        k = kernel()
        parse_txt(cfg, "mods=irc")
        self.assertEqual(cfg.sets.mods, "irc")

    def test_parse2(self):
        k = kernel()
        parse_txt(cfg, "mods=irc,udp")
        self.assertEqual(cfg.sets.mods, "irc,udp")

    def test_edit(self):
        k = kernel()
        d = {"mods": "rss"}
        edit(cfg, d)
        self.assertEqual(cfg.mods, "rss")
