import json
from nameko.extensions import DependencyProvider
from fauxit.model.shotgundb import SGDB
from fauxit.model.levelspec import LevelSpec

SHOTGUN = SGDB()

class ShotgunDependencyProvider(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return SHOTGUN