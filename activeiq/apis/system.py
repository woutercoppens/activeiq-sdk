from typing import Dict
from .api import PublicApi

class System(PublicApi):

    # def __init__(self, api, *args, **kwargs):
    #     self.api = api

    def list(
            self, 
            level: str
        ) -> Dict: 
        """
        Parameters
        Name	Description
        level	 Identifies the level for which information will be provided. Valid values are customer, site, and group.
        """
        path = '/v1/system/list/level/{}'.format(level)

        return self.request(path=path)

    def get_customers() -> Dict: 
        return self.list('customer')

    def get_sites() -> Dict: 
        return self.list('site')

    def get_groups() -> Dict: 
        return self.list('group')