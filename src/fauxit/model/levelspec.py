import re
from os.path import (join, sep)
from os import environ
from fauxit.settings import *
from fauxit.model.level import Level
from fauxit.model.level_name_validator import LevelNameValidator

init_env()

def default_validator(name, *args, **kwargs):
    return name

class LevelSpec(object): #(dict):
    """fake levelspec"""
    validate = LevelNameValidator.validate

    def __init__(self, show, sequence=None, shot=None):
        self.show = self.validate(show, Level.show)
        self.sequence = self.validate(sequence, Level.sequence)
        self.shot = self.validate(shot, Level.shot)


    def __eq(self, other):
        if self.shot == other.shot and \
        self.sequence == other.sequence and \
        self.show == other.show:
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other,LevelSpec):
            return False
        return self.__eq(other)

    def __ne__(self, other):
        if not isinstance(other, LevelSpec):
            return True
        return not self.__eq(other)

    def __add__(self, other):
        if self.shot is not None:
            raise RuntimeError("Cannot add a level to a full levelspec")
        if isinstance(other, basestring):
            return LevelSpec.from_str("{}.{}".format(str(self), other ))
        raise TypeError("{} must be of type string".format(str(other)))

    def leaf(self):
        """Return the deepest level in a levelspec. (eg given FOO.RD.0001 return 0001)"""
        if self.shot:
            return self.shot
        elif self.sequence:
            return self.sequence
        else:
            return self.show

    def parent(self):
        """Return the parent levelspec of the current Level, or none if the levelspec
        is a show"""
        if self.shot:
            return LevelSpec(self.show, self.sequence)
        if self.sequence:
            return LevelSpec(self.show)
        return None

    @classmethod
    def from_str(cls, levelspec):
        """Initialize a levelspec instance given a string of the
        form show[.seq[.shot]]"""

        if levelspec[0] == "." or levelspec[-1] == ".":
            raise ValueError("levelspec may not start with a '.': {}".format(levelspec))

        if " " in levelspec:
            raise ValueError("levelspec may not contain spaces: {}".format(levelspec))

        if ".." in levelspec:
            raise ValueError("levelspec may not contain contiguous dots: {}".format(levelspec))

        components = levelspec.split(".")

        if len(components) > 3:
            raise ValueError("levelspec may only contain at most 3 levels: {}".format(levelspec))

        return cls(*components)

    def _as_tuple(self):
        if self.shot:
            return (self.show, self.sequence, self.shot)
        elif self.sequence:
            return (self.show, self.sequence)
        else:
            return (self.show,)

    @staticmethod
    def root():
        return environ.get(DD_SHOWS_ROOT)

    def path(self, relpath=None):
        """Return the full path given a levelspec"""
        path = tuple(\
        filter( lambda x: x != "", self.root().split("/")) )\
        + self._as_tuple()
        if relpath:
            path = path + tuple(relpath.split(sep))
        return "{}{}".format(sep,join(*path))

    def __iter__(self):
        yield self
        if self.shot:
            yield self.__class__(self.show, self.sequence)
        if self.sequence:
            yield self.__class__(self.show)

    def __repr__(self):
        if self.shot:
            return "LevelSpec<{} {} {}>".format(self.show, self.sequence, self.shot)
        elif self.sequence:
            return "LevelSpec<{} {}>".format(self.show, self.sequence)
        else:
            return "LevelSpec<{}>".format(self.show)

    def __str__(self):
        if self.shot:
            return "{}.{}.{}".format(self.show, self.sequence, self.shot)
        elif self.sequence:
            return "{}.{}".format(self.show, self.sequence)
        else:
            return "{}".format(self.show)