from builtins import super
from oauthlib.oauth2 import BackendApplicationClient
# from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

from activeiq.clients.aiq_client import _AIQClient

# import var_dump

import logging

# logformat = '%(asctime)s [%(levelname)s] (%(name)s): %(message)s'
# logging.basicConfig(level=logging.DEBUG, format=logformat)
# log = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        if code is not None:
            self.code = code


class BackendClient(_AIQClient):
    def __init__(self, client_id, access_token, refresh_token):
        super().__init__(client_id, access_token, refresh_token)

        scope = [""]

        client = BackendApplicationClient(client_id=self.client_id)

        # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#third-recommended-define-automatic-token-refresh-and-update
        self.client = OAuth2Session(client=client, 
                                    token=self.token, 
                                    auto_refresh_url=self.refresh_url, 
                                    # headers=self.headers, 
                                    auto_refresh_kwargs=self.extra, 
                                    token_updater=self.token_saver,
                                    scope=scope
                                    )
        # self.client = OAuth2Session(client=client, 
        #                             token=self.token
        #                             )       