from nameko.rpc import RpcProxy
from nameko.rpc import rpc

from gateway import GatewayService

class GatewayRpcServiceHost(object):
    name = 'gateway_rpc_service'

    level_rpc   = RpcProxy('level_service')
    shotgun_rpc = RpcProxy('shotgun_service')

    def __init__(self):
        print dir(GatewayRpcServiceHost.level_rpc)

    @rpc
    def create_level(self, levelspec):
        gateway = GatewayService(self)
        gateway.build_level(levelspec)

