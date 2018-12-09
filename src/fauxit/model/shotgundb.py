from fauxit.model.levelspec import LevelSpec
from fauxit.model.level_name_validator import LevelNameValidator


class FauxLevel(object):
    """
    super class of SGDB, Project, Sequence which implements
    generic crud for children, iter, str,
    """
    child_cls = None
    def __init__(self, name, parent=None):
        self.children = {}
        self.name = name
        self.parent = parent

    def has_child(self, name):
        return self.children.has_key(str(name))

    def add_child(self, name):
        _name = str(name)
        if not self.has_child(name):
            self.children[_name] = self.__class__.child_cls(_name, self)
        return self.children[_name]

    def remove_child(self, name):
        _name = str(name)
        return self.children.pop(_name, None)

    def child(self, name):
        _name = str(name)
        return self.children[_name]

    def __iter__(self):
        for child in self.children.itervalues():
            yield child

    def __str__(self):
        return self.name

    @property
    def fullname(self):
        if self.parent is None:
            return self.name
        else:
            return "{}.{}".format( self.parent.fullname , self.name)

class Shot(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return self.name

    @property
    def fullname(self):
        if self.parent is None:
            return self.name
        else:
            return "{}.{}".format( self.parent.fullname , self.name)

class Sequence(FauxLevel):
    child_cls = Shot
    def __init__(self, name, parent=None):
        super(Sequence,self).__init__(name,parent)

    def has_shot(self, name):
        return self.has_child(name)

    def add_shot(self,name):
        return self.add_child(name)

    def remove_shot(self, name):
        return self.remove_child(name)

    def shot(self,name):
        return self.children[name]

    @property
    def shots(self):
        return self.children.__iter__()


class Project(FauxLevel):
    child_cls = Sequence

    def __init__(self, name, parent=None):
        super(Project,self).__init__(name,parent)
        self.assets = {}

    def has_asset(self, name):
        return self.assets.has_key(name)

    def add_asset(self, name):
        self.assets[name] = Asset(name)
        return self.assets[name]

    def remove_asset(self, name):
        return self.assets.pop(name, None)

    def asset(self,name):
        return self.assets[name]

    def has_sequence(self, name):
        return self.has_child(name)

    def add_sequence(self,name):
        return self.add_child(name)

    def remove_sequence(self, name):
        return self.remove_child(name)

    def sequence(self,name):
        return self.children[name]

    @property
    def sequences(self):
        return self.children.__iter__()


class Asset(object):
    def __init__(self,name):
        self.name = name


class SGDB(FauxLevel):
    child_cls = Project
    def __init__(self):
        super(SGDB,self).__init__("shotgun", None)

    def has_project(self, name):
        return self.has_child(name)

    def add_project(self, name):
        return self.add_child(name)

    def remove_project(self, name):
        return self.remove_child(name)

    def project(self, name):
        return self.children[name]

    def has_level(self, level):
        levelspec = LevelSpec.from_str(level)
        SGLEVEL = self
        has = False
        for idx, level in enumerate(reversed([x for x in levelspec])):
            if idx == 0:
                has = SGLEVEL.has_child(level)
                if has:
                    SGLEVEL = SGLEVEL.child(level)
            elif idx == 1:
                has = SGLEVEL.has_child(level)
                if has:
                    SGLEVEL = SGLEVEL.child(level)
            elif idx == 2:
                has = SGLEVEL.has_child(level)
                if has:
                    SGLEVEL = SGLEVEL.child(level)
        return has

    def add_level(self, level):
        levelspec = LevelSpec.from_str(level)
        SGL = self
        for level in reversed([x for x in levelspec]):
            print "create", level
            SGL = SGL.add_child(str(level.leaf() ))
        return SGL

    def remove_level(self, level):
        levelspec = LevelSpec.from_str(level)
        parent = levelspec.parent()
        if parent:
            self.level(parent).remove_child(levelspec.leaf())
        else:
            self.remove_child(level)

    def level(self, levelspec):
        """given a levelspec str, return an instance of Project, Sequence, or Shot"""
        levelspec = LevelSpec.from_str(levelspec)
        if levelspec.shot:
            return self.project(levelspec.show)\
            .sequence(levelspec.sequence)\
            .shot(levelspec.shot)
        if levelspec.sequence:
            return self.project(levelspec.show)\
            .sequence(levelspec.sequence)
        if levelspec.show:
            return self.project(levelspec.show)
        raise RuntimeError("unable to decode levelspec: {}".format(levelspec))

    def child_levels(self, level):
        return [child for child in self.level(level)]

    @property
    def projects(self):
        return self.children.__iter__()