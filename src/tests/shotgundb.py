import unittest
import os
import sys
pth = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pth)
from fauxit.model.shotgundb import FauxLevel, Shot, Sequence


class FauxLevelP(FauxLevel):

    def __init__(self, name):
        super(FauxLevelP,self).__init__(name)
FauxLevelP.child_cls = FauxLevelP

class FauxLevelTest(unittest.TestCase):
    """testing FauxLevel"""
    def test_has_child(self):
        fl = FauxLevelP("FOO")
        fl.add_child("BAR")
        self.assertTrue(fl.has_child("BAR"))
        self.assertFalse(fl.has_child("DONT"))

    def test_add_child(self):
        fl = FauxLevelP("FOO")
        fl.add_child("BAR")
        self.assertEqual(len(fl.children),1)
        self.assertTrue(fl.has_child("BAR"))

    def test_remove_child(self):
        fl = FauxLevelP("FOO")
        fl.add_child("BAR")
        child = fl.remove_child("BAR")
        self.assertEqual(len(fl.children), 0)
        self.assertEqual(child.name, "BAR")

    def test_remove_child_nonext(self):
        fl = FauxLevelP("FOO")
        fl.add_child("BAR")
        child = fl.remove_child("BLA")
        self.assertEqual(len(fl.children), 1)
        self.assertEqual(child, None)

    def test_child(self):
        fl = FauxLevelP("FOO")
        fl.add_child("BAR")
        self.assertEqual(len(fl.children), 1)
        child = fl.child("BAR")
        self.assertEqual(child.name, "BAR")
        self.assertEqual(len(fl.children), 1)


class ShotTest(unittest.TestCase):
    def test_init(self):
        shot = Shot("0001")
        self.assertEqual(shot.name, "0001")

    def test_str(self):
        shot = Shot("0001")
        self.assertEqual(str(shot), "0001")

class SequenceTest(unittest.TestCase):
    def test_init(self):
        seq = Sequence("RD")
        self.assertEqual(seq.name, "RD")
        self.assertEqual(str(seq), "RD")

    def test_add_shot(self):
        seq = Sequence("RD")
        self.assertEqual(len(seq.children), 0)

        seq.add_shot("0001")
        self.assertEqual(len(seq.children), 1)
        self.assertTrue(seq.has_child("0001"))

    def test_remove_shot(self):
        seq = Sequence("RD")
        self.assertEqual(len(seq.children), 0)
        seq.add_shot("0001")
        self.assertEqual(len(seq.children), 1)
        shot = seq.remove_shot("0001")
        self.assertEqual(len(seq.children),0)
        self.assertEqual(shot.name, "0001")

if __name__ == '__main__':
    unittest.main()