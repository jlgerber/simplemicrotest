from nameko.rpc import rpc
from shotgundb import SGDB
from levelspec import LevelSpec


SHOTGUN = SGDB()

class ShotgunService(object):
    name = "shotgun_service"

    @rpc
    def add_level(self, level):
        SHOTGUN.add_level(level)

    @rpc
    def has_level(self, level):
        return SHOTGUN.has_level(level)




