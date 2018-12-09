# call the gateway
from nameko.standalone.rpc import ClusterRpcProxy
config = {
'AMQP_URI':  "pyamqp://guest:guest@localhost"
}

class Caller(object):

    def create_level(self, level):
        print "creating a level"
        with ClusterRpcProxy(config) as cluster_rpc:
            cluster_rpc.gateway_rpc_service.create_level(level)