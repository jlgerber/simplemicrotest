import re
from os.path import (join, sep)
from os import environ
from fauxit.settings import *
from fauxit.model.level import Level
from fauxit.model.level_name_validator import LevelNameValidator

init_env()

def default_validator(name, *args, **kwargs):
    return name

class LevelSpec(object):
    """fake levelspec"""
    validate = LevelNameValidator.validate

    def __init__(self, show, sequence=None, shot=None):
        self.show = self.validate(show, Level.show)
        self.sequence = self.validate(sequence, Level.sequence)
        self.shot = self.validate(shot, Level.shot)

    def leaf(self):
        if self.shot:
            return self.shot
        elif self.sequence:
            return self.sequence
        else:
            return self.show

    def parent(self):
        if self.shot:
            return self.sequence
        if self.sequence:
            return self.show
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
        path = tuple(self.root().split("/")) + self._as_tuple()
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