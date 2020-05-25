import os
import time
from activeiq.clients.api import BackendClient

if __name__ == "__main__":
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # access_token = input("Enter Access Token:")
    refresh_token = input("Enter Refresh Token")

    token = {
    #     'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': '-30',     # initially 3600, need to be updated by you   
    }
    om_cloud = BackendClient("DEV_CLIENT_ID",
                             token
                            )
    om_cloud.get_token()
    installs = om_cloud.installations()