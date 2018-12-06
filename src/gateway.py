import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GatewayService:
    name = 'gateway'

    level_rpc = RpcProxy('level_service')
    shotgun_rpc = RpcProxy('shotgun_service')

    @http('GET', '/level/<string:levelspec>')
    def get_level(self, request, levelspec):

        if request.args.has_key("create") \
            and request.args.get("create").lower() == "true":
            try:
                self.shotgun_rpc.add_level(levelspec)
                self.level_rpc.mklevel(levelspec)
            except Exception as e:
                #roll back
                raise
        path = self.level_rpc.path(levelspec)
        has_level = self.shotgun_rpc.has_level(levelspec)
        shotgun_id = levelspec if has_level else "None"
        return json.dumps({'path': path, 'shotgun_id': shotgun_id})