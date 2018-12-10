import setup
setup.setup()

import unittest
from fauxit.model.shotgundb import FauxLevel, Shot, Sequence, Project, Asset, SGDB


class FauxLevelP(FauxLevel):

    def __init__(self, name, parent=None):
        super(FauxLevelP,self).__init__(name,parent)
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

    def test_fullname(self):
        fl = FauxLevelP("FOO")
        child = fl.add_child("BAR")
        gchild = child.add_child("BLA")
        fullname = gchild.fullname
        self.assertEqual(fullname, "FOO.BAR.BLA")

    def test_fullname_noparent(self):
        fl = FauxLevelP("FOO")
        fullname = fl.fullname
        self.assertEqual(fullname, "FOO")

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

    def test_remove_shot_nonextant(self):
        seq = Sequence("RD")
        self.assertEqual(len(seq.children), 0)
        seq.add_shot("0001")
        self.assertEqual(len(seq.children), 1)
        shot = seq.remove_shot("0002")
        self.assertEqual(len(seq.children),1)
        self.assertEqual(shot, None)

    def test_shot(self):
        seq = Sequence("RD")
        self.assertEqual(len(seq.children), 0)
        seq.add_shot("0001")
        self.assertEqual(len(seq.children), 1)
        shot = seq.shot("0001")
        self.assertEqual(len(seq.children),1)
        self.assertEqual(shot.name, "0001")

    def test_shot_nonextant(self):
        seq = Sequence("RD")
        self.assertEqual(len(seq.children), 0)
        seq.add_shot("0001")
        self.assertEqual(len(seq.children), 1)
        with self.assertRaises(KeyError):
            shot = seq.shot("0002")
        self.assertEqual(len(seq.children),1)

    def test_shots_decorator(self):
        seq = Sequence("RD")
        seq.add_shot("0001")
        seq.add_shot("0002")
        seq.add_shot("0003")
        results = [shot for shot in seq]
        expect = [Shot("0001"), Shot("0002"), Shot("0003")]
        for x,y in zip(results,expect):
            self.assertEqual(x.name, y.name)

    def test_fullname(self):
        seq = Sequence("RD")
        shot = seq.add_shot("0001")
        self.assertEqual(shot.fullname, "RD.0001")

class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.proj = Project("MONKEYKING")
    def test_init(self):
        self.assertEqual(self.proj.name, "MONKEYKING")
        self.assertEqual(str(self.proj), "MONKEYKING")

    def test_has_asset(self):
        self.proj.add_asset("fred")
        self.assertTrue(self.proj.has_asset("fred"))

    def test_add_asset(self):
        self.proj.add_asset("fred")
        self.assertTrue(self.proj.assets.has_key("fred"))

    def test_remove_asset(self):
        self.proj.add_asset("fred")
        asset = self.proj.remove_asset("fred")
        self.assertEqual(asset.name, "fred")
        self.assertEqual(len(self.proj.assets),0)

    def test_remove_asset_nonextant(self):
        self.proj.add_asset("fred")
        asset = self.proj.remove_asset("barney")
        self.assertEqual(asset, None)
        self.assertEqual(len(self.proj.assets),1)

    def test_asset(self):
        """callign asset should return the asset but
        it should not remove it from the project"""
        self.proj.add_asset("fred")
        asset = self.proj.asset("fred")
        self.assertEqual(asset.name, "fred")
        self.assertTrue(self.proj.has_asset("fred"))

    def test_asset_nonextant(self):
        """callign asset should return the asset but
        it should not remove it from the project"""
        self.proj.add_asset("fred")
        with self.assertRaises(KeyError):
            asset = self.proj.asset("bar")
        self.assertTrue(self.proj.has_asset("fred"))

    def test_add_sequence(self):
        self.assertEqual(len(self.proj.children), 0)
        self.proj.add_sequence("RD")
        self.assertEqual(len(self.proj.children), 1)
        self.assertTrue(self.proj.has_child("RD"))

    def test_remove_sequence(self):
        self.assertEqual(len(self.proj.children), 0)
        self.proj.add_sequence("RD")
        self.assertEqual(len(self.proj.children), 1)
        sequence = self.proj.remove_sequence("RD")
        self.assertEqual(len(self.proj.children),0)
        self.assertEqual(sequence.name, "RD")

    def test_remove_sequence_nonextant(self):
        self.assertEqual(len(self.proj.children), 0)
        self.proj.add_sequence("RD")
        self.assertEqual(len(self.proj.children), 1)
        sequence = self.proj.remove_sequence("AA")
        self.assertEqual(len(self.proj.children),1)
        self.assertEqual(sequence, None)

    def test_sequence(self):
        self.assertEqual(len(self.proj.children), 0)
        self.proj.add_sequence("RD")
        self.assertEqual(len(self.proj.children), 1)
        sequence = self.proj.sequence("RD")
        self.assertEqual(len(self.proj.children),1)
        self.assertEqual(sequence.name, "RD")

    def test_sequence_nonextant(self):
        self.assertEqual(len(self.proj.children), 0)
        self.proj.add_sequence("RD")
        self.assertEqual(len(self.proj.children), 1)
        with self.assertRaises(KeyError):
            sequence = self.proj.sequence("AA")
        self.assertEqual(len(self.proj.children),1)

    def test_sequences_decorator(self):
        self.proj.add_sequence("RD")
        self.proj.add_sequence("AA")
        self.proj.add_sequence("BB")
        results = [seq for seq in self.proj]
        expect = [Sequence("RD"), Sequence("AA"), Sequence("BB")]
        for x,y in zip(results, expect):
            self.assertEqual(x.name, y.name)

    def test_fullname(self):
        seq = self.proj.add_sequence("RD")
        shot = seq.add_shot("0001")
        self.assertEqual(shot.fullname, "MONKEYKING.RD.0001")

class TestSGDB(unittest.TestCase):
    def setUp(self):
        self.db = SGDB()

    def test_init(self):
        self.assertEqual(self.db.name, "shotgun")

    def test_has_project(self):
        self.db.add_child("FOO")
        self.db.add_child("BAR")
        self.assertTrue(self.db.has_project("FOO"))
        self.assertTrue(self.db.has_project("BAR"))
        self.assertFalse(self.db.has_project("YADAYADAYADA"))

    def test_add_project(self):
        self.db.add_project("FOO")
        self.assertTrue(self.db.has_child("FOO"))
        self.assertFalse(self.db.has_child("NONE"))

    def test_remove_project(self):
        self.db.add_child("FOO")
        proj = self.db.remove_project("FOO")
        self.assertEqual(proj.name, "FOO")
        self.assertEqual(len(self.db.children), 0)
        self.assertFalse(self.db.has_child("FOO"))

    def test_project(self):
        self.db.add_child("FOO")
        self.db.add_child("BAR")
        proj = self.db.project("FOO")
        self.assertEqual(proj.name, "FOO")
        self.assertTrue(self.db.has_child("FOO"))

    def test_has_level(self):
        self.db.add_child("FOO")
        self.db.add_child("BAR")
        self.assertTrue(self.db.has_level("FOO"))
        self.assertTrue(self.db.has_level("BAR"))
        self.assertFalse(self.db.has_level("YADAYADAYADA"))

    def test_add_level(self):
        self.db.add_level("FOO.RD")
        self.assertTrue(self.db.has_child("FOO"))
        proj = self.db.children.pop("FOO")
        self.assertEqual(proj.name, "FOO")
        self.assertEqual(len(proj.children),1)
        seqs = [x for x in proj.sequences]
        self.assertEqual(seqs[0], "RD")
        self.assertTrue(proj.has_sequence("RD"))

    def remove_level(self):
        """ """
    def test_level(self):
        """ """
    def test_child_levels(self):
        """ """
    def test_projects(self):
        """ """

if __name__ == '__main__':
    unittest.main()