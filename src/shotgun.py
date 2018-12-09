import json
from nameko.rpc import rpc
from nameko.web.handlers import http

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

    def _assets(self,project):
        return SHOTGUN.project(project).assets

    @rpc
    def assets(self, project):
        return self._assets(project)

    @http('GET', '/sgassets/<string:project>')
    def get_assets_http(self, request, project):
        assets = self._assets(project)
        return json.dumps({ 'assets': assets})

    def _projects(self):
        return SHOTGUN.children.keys()

    @rpc
    def projects(self):
        return self._projects()

    @http('GET', '/sgprojects')
    def get_projects_http(self, request):
        projects= self._projects()
        return json.dumps({ 'projects': projects})

    @rpc
    def child_levels(self, level=None):
        return self._projects() if level is None else [str(x) for x in SHOTGUN.child_levels(level)]
