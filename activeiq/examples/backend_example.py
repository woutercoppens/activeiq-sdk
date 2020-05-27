import os
import time
from activeiq.clients.api import BackendClient

import logging

# import var_dump

LOG_FILENAME = 'example.log'
# logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logformat = '%(asctime)s [%(levelname)s] (%(name)s): %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logformat)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    access_token = input("Enter Access Token: ")
    # access_token = 'dddd'
    refresh_token = input("Enter Refresh Token: ")

    aiq = BackendClient("DEV_CLIENT_ID",
                            access_token,
                            refresh_token
                            )
    aiq.refresh_token()
    customers = aiq.system_list('customer')
    