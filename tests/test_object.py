# OLIB - object library
#
#

import ol
import types
import unittest

class Test_Object(unittest.TestCase):

    def test_empty(self):
        o = ol.Object()
        self.assertTrue(not o) 

    def test_final(self):
        o = ol.Object()
        o.last = "bla"
        ol.dbs.last(o)
        self.assertEqual(o.last, "bla")

    def test_stamp(self):
        o = ol.Object()
        ol.save(o)
        self.assertTrue(o.__stp__)

    def test_attribute(self):
        o = ol.Object()
        o.bla = "test"
        p = ol.save(o)
        oo = ol.Object()
        ol.load(oo, p)
        self.assertEqual(oo.bla, "test")

    def test_changeattr(self):
        o = ol.Object()
        o.bla = "test"
        p = ol.save(o)
        oo = ol.Object()
        ol.load(oo, p)
        oo.bla = "mekker"
        pp = ol.save(oo)
        ooo = ol.Object()
        ol.load(ooo, pp)
        self.assertEqual(ooo.bla, "mekker")

    def test_last(self):
        o = ol.Object()
        o.bla = "test"
        ol.save(o)
        oo = ol.Object()
        ol.dbs.last(oo)
        self.assertEqual(oo.bla, "test")

    def test_lastest(self):
        o = ol.Object()
        o.bla = "test"
        ol.save(o)
        oo = ol.Object()
        ol.dbs.last(oo)
        oo.bla = "mekker"
        ol.save(oo)
        ooo = ol.Object()
        ol.dbs.last(ooo)
        self.assertEqual(ooo.bla, "mekker")
