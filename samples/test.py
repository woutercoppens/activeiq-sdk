import os
import time
import activeiq

import logging

import var_dump

#from dict_to_csv import extract_header, transform
import csv
import pandas as pd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

if __name__ == "__main__":
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    access_token = input("Enter Access Token: ")
    # access_token = 'dddd'
    refresh_token = input("Enter Refresh Token: ")

    aiq = activeiq.ActiveIQClient(refresh_token, access_token)
    #aiq.get_refresh_token()
    customers = aiq.system.list('customer')
    #var_dump(customers)

    k = customers['customers']
    l = k['list']
    
    logging.debug(l)
    # headers = extract_header(l)
    # output = transform(l)

    df = pd.DataFrame(l)
    df.to_csv('customers.csv')

    # with open('customers.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(output)