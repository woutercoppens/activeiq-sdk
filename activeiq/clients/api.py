import logging

from builtins import super
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session

logger = logging.getLogger("activeiq")

class APIError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        if code is not None:
            self.code = code


class BackendClient(_AIQClient):
    def __init__(self, refresh_token):
        super().__init__(client_id, refresh_token)

        self.scope = "control view"
        extra = {'client_id': self.client_id,
                 'token': self.token}

        client = BackendApplicationClient(client_id=self.client_id)
        self.client = OAuth2Session(client=client, auto_refresh_url=self.token_url, auto_refresh_kwargs=extra, token_updater=self.token_saver)
        #self.client = OAuth2Session(client=client, token=token)


class _AIQClient(object):
    PREFIX = '/api/v1'

    def __init__(self, client_id, refresh_token):
        self.client = None
        self.client_id = client_id

        self.token = {
            'access_token': '',
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': '-30',     # initially 3600, need to be updated by you   
        }

        self.server = "api.activeiq.netapp.com"
        self.token_url = self._get_url('/v1/tokens/accessToken')

    def get_token(self):
        self.token = self.client.get_token(token_url=self.token_url, client_id=self.client_id, token=self.token)

    def token_saver(self, token):
        self.token = token

    def _get_url(self, endpoint):
        #endpoint should always start with a /
        return 'https://{}{}'.format(self.server, endpoint)
    
    def _get_data(self, url):
        response = self.client.get(url)
        data = response.json().get('data')
        return data       

    def installations_by_group(self, installation_group):
        url = self._get_url('/base/installationgroups/{}/installations'.format(installation_group))
        response = self.client.get(url)
        data = response.json().get('data')
        return data

