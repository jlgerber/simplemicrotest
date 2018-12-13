import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class ShotgunHttpService(object):
    name = "shotgun_http_service"

    shotgun_rpc = RpcProxy('shotgun_service')

    @http('GET', '/sgprojects')
    def get_projects_http(self, request):
        projects= self.shotgun_rpc.projects()
        return json.dumps({ 'projects': projects})


    @http('GET', '/sgassets/<string:project>')
    def get_assets_http(self, request, project):
        assets = self.shotgun_rpc.assets(project)
        return json.dumps({ 'assets': assets})