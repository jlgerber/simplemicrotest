from levelspec import LevelSpec


class FauxLevel(object):
    child_cls = None
    def __init__(self, name):
        self.children = {}
        self.name = name

    def has_child(self, name):
        return self.children.has_key(str(name))

    def add_child(self, name):
        _name = str(name)
        if not self.has_child(name):
            self.children[_name] = self.__class__.child_cls(_name)
        return self.children[_name]

    def child(self, name):
        _name = str(name)
        return self.children[_name]

    def __iter__(self):
        for child in self.children.itervalues():
            yield child

    def __str__(self):
        return self.name

class Shot(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name

class Sequence(FauxLevel):
    child_cls = Shot
    def __init__(self, name):
        super(Sequence,self).__init__(name)

    def has_shot(self, name):
        return self.has_child(name)

    def add_shot(self,name):
        return self.add_child(name)

    def shot(self,name):
        return self.children[name]

class Project(FauxLevel):
    child_cls = Sequence

    def __init__(self, name):
        super(Project,self).__init__(name)

    def has_sequence(self, name):
        return self.has_child(name)

    def add_sequence(self,name):
        return self.add_child(name)

    def sequence(self,name):
        return self.children[name]


class SGDB(FauxLevel):
    child_cls = Project
    def __init__(self):
        super(SGDB,self).__init__("shotgun")

    def has_project(self, name):
        return self.has_child(name)

    def add_project(self, name):
        return self.add_child(name)

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
            SGL = SGL.add_child(str(level))
        return SGL
