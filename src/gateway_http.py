import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from gateway import GatewayService

class GatewayHttpServiceHost(object):
    name = 'gateway_http_service'

    level_rpc   = RpcProxy('level_service')
    shotgun_rpc = RpcProxy('shotgun_service')

    @http('GET', '/levels/<string:levelspec>')
    def get_level_http(self, request, levelspec):
        """
        handle the level route
        """
        gateway = GatewayService(self)

        if request.args.has_key("create") \
            and request.args.get("create").lower() == "true":
            # generate level and shotgun entry if user asks for it.
            # throw an exception after rolling back if necessary
            gateway.build_level(levelspec)
        return gateway.get_level(levelspec)

    @http('GET', '/projects/<string:levelspec>')
    def get_project_http(self, request, levelspec):
        """
        handle the level route
        """
        gateway = GatewayService(self)

        if "." in levelspec:
            raise KeyError("Invalid project passed in")

        if request.args.has_key("create") \
            and request.args.get("create").lower() == "true":
            # generate level and shotgun entry if user asks for it.
            # throw an exception after rolling back if necessary
            gateway.build_level(levelspec)
        return gateway.get_level(levelspec)

    @http('GET', '/projects')
    def get_projects_http(self, request):
        """
        retrieve projects
        """
        gateway = GatewayService(self)
        return gateway.get_projects()

    @http('GET', '/projects/<string:project>/assets/<string:asset>')
    def get_assets_for_project_http(self, request, project, asset):
        """
         projects
        """
        gateway = GatewayService(self)

        return gateway.get_projects()

