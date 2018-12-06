from nameko.rpc import rpc
from fauxit.model.shotgundb import SGDB
from fauxit.model.levelspec import LevelSpec


SHOTGUN = SGDB()

class ShotgunService(object):
    name = "shotgun_service"

    @rpc
    def add_level(self, level):
        SHOTGUN.add_level(level)

    @rpc
    def has_level(self, level):
        return SHOTGUN.has_level(level)

    @rpc
    def add_asset(self, project, name):
        if not SHOTGUN.has_project(project):
            raise KeyError("project: {} does not exist in shotgun".format(project))
        SHOTGUN.project(project).add_asset(name)

    @rpc
    def assets(self, project):
        return SHOTGUN.project(project).assets

    def _projects(self):
        return SHOTGUN.children.keys()
    @rpc
    def projects(self):
        return self._projects()

    @rpc
    def child_levels(self, level=None):
        return self._projects() if level is None else [str(x) for x in SHOTGUN.child_levels(level)]
