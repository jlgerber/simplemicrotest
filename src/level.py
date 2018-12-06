from nameko.rpc import rpc
import os, errno
import shutil
from fauxit.model.levelspec import LevelSpec

class LevelService(object):
    name = "level_service"


    def _path(self, level, relpath):
        levelspec = LevelSpec.from_str(level)
        path = levelspec.path(relpath)
        return path
    @rpc
    def path(self, level, relpath=None):
        return self._path(level, relpath)

    @rpc
    def ls(self, level=None, relpath=None):
        path = self.root() if level is None else self._path(level, relpath)
        return os.listdir(path)

    @rpc
    def root(self):
        return LevelSpec.root()

    @rpc
    def mk(self, newdir, mode=0777):
        try:
            os.makedirs(newdir, mode)
        except OSError, err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(newdir):
                raise
        return newdir


    @rpc
    def mklevel(self, level, relpath=None, mode=0777):
        try:
            lsp = LevelSpec.from_str(level)
            newdir = lsp.path(relpath)
            os.makedirs(newdir, mode)
        except OSError, err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(newdir):
                raise
        return newdir


    @rpc
    def rm(self, targetdir):
        try:
            shutil.rmtree(targetdir)
        except OSError, err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(targetdir):
                raise
        return targetdir


