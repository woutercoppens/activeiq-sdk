import logging

try:
    import simplejson as json
except ImportError:
    import json

import requests
from oauthlib.oauth2 import TokenExpiredError, MissingTokenError


import traceback
# logger = logging.getLogger("activeiq")

class _AIQClient(object):

    def __init__(self, client_id, access_token, refresh_token):
        self.client = None
        self.client_id = client_id

        self.token = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': '-30',     # initially 3600, need to be updated by you   
        #    'expires_in': '300',       
        }

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # extra = {'client_id': self.client_id}
        self.extra = {} 

        self.server = "api.activeiq.netapp.com"
        self.refresh_url = self._get_url('/v1/tokens/accessToken')

    # def fetch_token(self):
    #    self.token = self.client.fetch_token(token_url=self.refresh_url, client_id=self.client_id, token=self.token, include_client_id=True)

    def refresh_token(self):
        """Manual refresh."""
        # https://requests-oauthlib.readthedocs.io/en/latest/api.html
        logging.debug('Called update_token')
 
        headers = {
                  "Accept": "application/json",
                  "Content-Type": "application/json",
                  "refreshToken": self.token['refresh_token']
        }
        # r =self.client.request(method='POST', url=self.refresh_url, headers=headers)
        try:
            self.token = self.client.refresh_token(token_url=self.refresh_url, refresh_token=self.refresh_token, headers=headers, include_client_id=False, body="")
            # self.token = self.client.fetch_token(token_url=self.refresh_url, headers=headers )

        except MissingTokenError as e:
            traceback.print_stack()
            print(repr(traceback.extract_stack()))
            print(repr(traceback.format_stack()))

    def token_saver(self, token):
        self.token = token

    def _get_url(self, endpoint):
        #endpoint should always start with a /
        return 'https://{}{}'.format(self.server, endpoint)
    
    def _get_responce(self, url):
        try:
            # r = self.client.get(url)
            headers = {
                      "Accept": "application/json",
                      "Content-Type": "application/json",
                      "authorizationToken": self.token['access_token']
            }
            r = self.client.request(method='GET', url=url, headers=headers)

            if r.status_code == 401:
                # Calling an API with an expired access token will result in a
                # HTTP status code of 401 (Unauthorized).
                raise TokenExpiredError

        except TokenExpiredError as e:
            self.refresh_token()
            r = self._get_responce(url)

        if r.status_code == 200:
            return r.message       

        return None

    def system_list(self, level):
        url = self._get_url('/v1/system/list/level/{}'.format(level))
        r = self._get_responce(url)
        return r
