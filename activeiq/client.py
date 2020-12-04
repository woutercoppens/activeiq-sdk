# -*- coding: utf-8 -*-
# ===============================
#      NetApp ActiveIQ API wrapper
# ===============================
import os
import logging
from urllib import response
import requests

from urllib.parse import urljoin

from cached_property import cached_property

# Imports
import re
# from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.error import HTTPError
import warnings
from six import string_types



try:
    import simplejson as json
except ImportError:
    import json

import var_dump
# Base API wrapper class

from .apis import ClusterView 
from .apis import System

class ActiveIQClient(object):
    """
    ActiveIQ is wrapper for NetApp ActiveIQ API.
    """

    # clusterview = ClusterView
    # systems = System 

    def __init__(self, refresh_token: str, access_token: str = None
    ):
        self._base_url = 'https://api.activeiq.netapp.com'

        if not refresh_token:
            raise ValueError("Refresh Token must be provided. You can obtain one for free at {}".format(self._base_url))

        if refresh_token and not isinstance(refresh_token, string_types):
            raise TypeError("refresh_token parameter must be a string value")

        if access_token and not isinstance(access_token, string_types):
            raise TypeError("access_token parameter must be a string value")

        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_refresh_token(self):
        """Manual refresh."""
        refresh_url = self._url('v1/tokens/accessToken')

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = {
                  "refresh_token": self.refresh_token
        }

        r = requests.post(refresh_url,json=payload,headers=headers)
        r.raise_for_status()

        logging.debug("Request to fetch token completed with status %s.", r.status_code)
        logging.debug("Request url was %s", r.request.url)
        logging.debug("Request headers were %s", r.request.headers)
        logging.debug("Request body was %s", r.request.body)
        logging.debug("Response headers were %s and content %s.", r.headers, r.text)

        if r.status_code == 200:
            logging.debug('Successfully obtained new tokens')
            json_response  = r.json()
            logging.debug(json_response)
            if 'access_token' in json_response:
                self.access_token = json_response.get('access_token')
                logging.debug("Obtained access_token %s.", self.access_token)

            if 'refresh_token' in json_response:
                self.refresh_token = json_response.get('refresh_token')
                logging.debug("Obtained refresh_token %s.", self.refresh_token)
        else:
            logging.error("Error: %s", r.text)
            exit

    # def _get_url(self, endpoint):
    #     #endpoint should always start with a /
    #     return 'https://{}{}'.format(self.server, endpoint)

    # def _get_response(self, url):
    #     headers = {
    #         "Accept": "application/json",
    #         'authorizationtoken': self.access_token
    #     }

    #     try:
    #         r = request.get(url, headers=headers)

    #         if r.status_code == 401:
    #             # Calling an API with an expired access token will result in a
    #             # HTTP status code of 401 (Unauthorized).
    #             raise TokenExpiredError

    #     except TokenExpiredError as e:
    #         self.get_refresh_token()
    #         r = self._get_responce(url)

    #     if r.status_code == 200:
    #         return r.message       

    #     return None

    # def fetch_data(self, endpoint):
    #     url = self._get_url(endpoint)
    #     r = self._get_responce(url)
    #     return self.__adapt_response_content(r)

    def _url(self, *path):
        url = self._base_url
        for p in path:
            url = urljoin(url, p)
        logging.debug("_url: %s.", url)
        return url

    # def _cursor_iterator(self, response_json, path, method, data, headers):
    #     for i in response_json['items']:
    #         yield i

    #     data = dict(data or {})

    #     while 'cursor' in response_json:
    #         data['cursor'] = response_json['cursor']
    #         response = self._raw_request(path, method, data, headers)
    #         response.raise_for_status()
    #         response_json = response.json()
    #         for i in response_json['items']:
    #             yield i

    def _raw_request(self, path, method='GET', data=None, headers=None):
        url = self._url(path)
        headers = headers or {}
        headers['Accept'] ='application/json'
        headers['authorizationtoken'] = '%s' % self.access_token
        if method == 'GET':
            return requests.get(url, params=data, headers=headers)

        if method == 'POST':
            return requests.post(url, json=data, headers=headers)

        if method == 'PUT':
            return requests.put(url, json=data, headers=headers)

        if method == 'PATCH':
            return requests.patch(url, json=data, headers=headers)

        if method == 'DELETE':
            return requests.delete(url, json=data, headers=headers)

        raise ValueError('Unsupported method "%s"' % method)
    
    def request(self, path, method='GET', data=None, headers=None):
        logging.debug('request path: %s', path)
        try: 
            response = self._raw_request(path, method, data, headers)
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            if response.status_code == 401 :
                self.get_refresh_token()
                response = self.request(path, method, data, headers)
            else:
                raise requests.exceptions.HTTPError
        
        return self.__adapt_response_content(response)

    def __adapt_response_content(self, response):
        """
        Check if response is a JSON and return it. Otherwise - return raw content
        :param response: Requests response
        :return: {} or raw content
        """
        if response is None:
            return {}

        # in case request() is called recursively, the response is already a dict object
        # so json.loads will fail
        if isinstance(response, dict):
            return response

        try:
            responseBody = json.loads(response.text)
        except:
            return response.content

        return responseBody

    @cached_property
    def system(self):
        return System(self)
