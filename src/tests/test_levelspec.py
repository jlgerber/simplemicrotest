import setup
setup.setup()
from os import environ

import unittest
from fauxit.model.levelspec import LevelSpec
from fauxit.settings import DD_SHOWS_ROOT

class TestLevelSpec(unittest.TestCase):

    def test_eq(self):
        ls = LevelSpec.from_str("FOO.RD.0001")
        other = "bla"
        self.assertFalse(ls == other)
        other = LevelSpec("FOO")
        self.assertFalse(ls == other)
        other = LevelSpec.from_str("FOO.RD.0001")
        self.assertTrue(ls == other)

    def test_neq(self):
        ls = LevelSpec.from_str("FOO.RD.0001")
        other = "bla"
        self.assertTrue(ls != other)
        other = LevelSpec("FOO")
        self.assertTrue(ls != other)
        other = LevelSpec.from_str("FOO.RD.0001")
        self.assertFalse(ls != other)

    def from_str_shot(self):
        ls = LevelSpec.from_str("FOO.RD.0001")
        expect = LevelSpec("FOO","RD","0001")
        self.assertEqual(ls,expect)

    def from_str_seq(self):
        ls = LevelSpec.from_str("FOO.RD")
        expect = LevelSpec("FOO","RD")
        self.assertEqual(ls,expect)

    def from_str_show(self):
        ls = LevelSpec.from_str("FOO")
        expect = LevelSpec("FOO")
        self.assertEqual(ls,expect)

    def from_str_bad(self):
        with self.assertRaises(KeyError):
            ls = LevelSpec.from_str("")

    def test_leaf(self):
        ls = LevelSpec.from_str("FOO.RD.0001")
        leaf = ls.leaf()
        expect = "0001"
        self.assertEqual(leaf, expect)

    def test_show_leaf(self):
        ls = LevelSpec.from_str("FOO")
        leaf = ls.leaf()
        expect = "FOO"
        self.assertEqual(leaf, expect)

    def test_parent_shot(self):
        ls = LevelSpec.from_str("FOO.RD.0001")
        leaf = ls.parent()
        expect = LevelSpec.from_str("FOO.RD")
        self.assertEqual(leaf, expect)

    def test_parent_seq(self):
        ls = LevelSpec.from_str("FOO.RD")
        leaf = ls.parent()
        expect = LevelSpec("FOO")
        self.assertEqual(leaf, expect)

    def test_parent_show(self):
        ls = LevelSpec.from_str("FOO")
        leaf = ls.parent()
        expect = None
        self.assertEqual(leaf, expect)

    def test_path_norelpath(self):
        """only valid for linux. i am lazy"""
        environ[DD_SHOWS_ROOT] = "/TEST"
        ls = LevelSpec.from_str("FOO.BAR.0001")
        expect = "/TEST/FOO/BAR/0001"
        self.assertEqual(ls.path(), expect)


    def test_path_relpath(self):
        """only valid for linux. i am lazy"""
        environ[DD_SHOWS_ROOT] = "/TEST"
        ls = LevelSpec.from_str("FOO.BAR.0001")
        expect = "/TEST/FOO/BAR/0001/bla/bla/bla"
        self.assertEqual(ls.path("bla/bla/bla"), expect)

    def test_path_relpath_sloppy(self):
        """only valid for linux. i am lazy"""
        environ[DD_SHOWS_ROOT] = "/TEST"
        ls = LevelSpec.from_str("FOO.BAR.0001")
        expect = "/TEST/FOO/BAR/0001/bla/bla/bla"
        self.assertEqual(ls.path("//bla////bla/bla"), expect)

if __name__ == '__main__':
    unittest.main()