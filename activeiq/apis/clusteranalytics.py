from typing import Dict
from .api import PublicApi

class ClusterView(PublicApi):

    # def __init__(self, api, *args, **kwargs):
    #     self.api = api

    def get_cluster_configuration(
            self, 
            uuid: str
        ) -> Dict: 
        """
        Parameters
        Name	Description
        uuid	Specifies the required cluster ID or UUID.
        """
        endpoint = '/v1/clusterview/get-cluster-configuration/{}'.format(uuid)

        return self.request(path=endpoint)
