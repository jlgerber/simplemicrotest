import json

class GatewayService(object):
    """Implement the business logic"""
    def __init__(self, gateway_service):
        self.gw = gateway_service

    def build_level(self, levelspec):
        """construct level in shotgun and on disk"""
        try:
            # shotgun
            self.gw.shotgun_rpc.add_level(levelspec)
            # level
            self.gw.level_rpc.mklevel(levelspec)
        except Exception as e:
            #roll back
            raise

    def get_level(self, levelspec):
        # get the full path to the levelspec from level
        path = self.gw.level_rpc.path(levelspec)
        # determine whether shotgun has the level
        has_level = self.gw.shotgun_rpc.has_level(levelspec)
        # generate a "shotgun id"
        shotgun_id = levelspec if has_level else "None"
        # return json
        return json.dumps({'path': path, 'shotgun_id': shotgun_id})

    def get_projects(self):
        projects = self.gw.shotgun_rpc.projects()
        return json.dumps({ 'projects': projects})

    def add_asset(self, project, asset):
        self.gw.shotgun_rpc.add_asset(project, asset)