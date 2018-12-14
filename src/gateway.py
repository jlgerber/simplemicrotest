import json
import errno
from fauxit.model.levelspec import LevelSpec

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

    def get_children(self, levelspec):
        # get the full path to the levelspec from level
        sgchildren = self.gw.shotgun_rpc.child_levels(levelspec)
        children = []
        for child in sgchildren:
            child_levelspec = LevelSpec.from_str(levelspec) + child
            children.append(str(child_levelspec))
        # return json

        return json.dumps({'child_levels': children})

    def delete_level(self, levelspec):
        removed = self.gw.level_rpc.rmlevel(levelspec)
        self.gw.shotgun_rpc.remove_level(levelspec)
        return removed

    def get_projects(self):
        projects = self.gw.shotgun_rpc.projects()
        return json.dumps({ 'projects': projects})

    def add_asset(self, project, asset):
        self.gw.shotgun_rpc.add_asset(project, asset)