import json
from nameko.rpc import rpc
from nameko.web.handlers import http

from fauxit.model.shotgundb import SGDB
from fauxit.model.levelspec import LevelSpec
from service_providers.shotgun import ShotgunDependencyProvider

#SHOTGUN = SGDB()

class ShotgunService(object):
    name = "shotgun_service"

    sg = ShotgunDependencyProvider()

    @rpc
    def add_level(self, level):
        self.sg.add_level(level)

    @rpc
    def has_level(self, level):
        return self.sg.has_level(level)

    @rpc
    def remove_level(self, level):
        self.sg.remove_level(level)

    @rpc
    def add_asset(self, project, name):
        if not self.sg.has_project(project):
            raise KeyError("project: {} does not exist in shotgun".format(project))
        self.sg.project(project).add_asset(name)

    def _assets(self,project):
        return self.sg.project(project).assets

    @rpc
    def assets(self, project):
        return self._assets(project)

    def _projects(self):
        return self.sg.children.keys()

    @rpc
    def projects(self):
        return self._projects()

    @rpc
    def child_levels(self, level=None):
        return self._projects() if level is None else [str(x) for x in self.sg.child_levels(level)]
