import json
from marshmallow import ValidationError
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from gateway import GatewayService
import schemas

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
        children= gateway.get_children(levelspec)
        return  children

    @http('DELETE', '/levels/<string:levelspec>')
    def delete_level_http(self, request, levelspec):
        """
        handle the level route
        """
        gateway = GatewayService(self)
        try:
            removed = gateway.delete_level(levelspec)
        except Exception as err:
            return 400, json.dumps({
                'error': 'BAD_REQUEST',
                'message': err.message
            })
        else:
            return 204 if removed == 1 else 200, ''

    @http('POST', '/levels')
    def post_level_http(self, request):
        """
        handle the level route
        """
        try:
            levelspec = schemas.LevelSpec(strict=True).loads(
                request.get_data(as_text=True)
            ).data['levelspec']
        except ValidationError as err:
            return 400, json.dumps({
                'error': 'BAD_REQUEST',
                'message': err.messages
            })
        gateway = GatewayService(self)
        gateway.build_level(levelspec)

        return 200, gateway.get_level(levelspec)

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
        """projects"""
        gateway = GatewayService(self)
        return gateway.get_projects()

