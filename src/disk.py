from nameko.rpc import rpc
import os, errno
import shutil
import .level

class LevelService(object):
    name = "level_service"

    @rpc
    def ls(self, level, relpath=None):
        return os.listdir(path)

    @rpc
    def mk(self, newdir, mode):
        try:
            os.makedirs(newdir, mode)
        except OSError, err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(newdir):
                raise
        return newdir


    @rpc
    def rm(self, targetdirs):
        try:
            shutil.rmdirs(targetdir)
        except OSError, err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(newdir):
                raise
        return newdir


