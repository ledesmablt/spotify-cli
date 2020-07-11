import os
import time
import json

import requests

from utils.exceptions import *
from utils.constants import CREDS_PATH, REFRESH_URI, API_URL

# credentials & api handler
class SpotifyHandler:
    def __init__(self):
        pass


    def get_credentials(self):
        if not os.path.exists(CREDS_PATH):
            return {}

        with open(CREDS_PATH) as f:
            creds = json.load(f)

        return creds


    def is_expired(self):
        creds = self.get_credentials()
        return int(time.time()) > creds.get('expires_on', 0)


    def refresh(self, auth_code=None):
        post_data = {}
        if auth_code:
            post_data = {'auth_code': auth_code}
        else:
            refresh_token = self.get_credentials().get('refresh_token')
            if refresh_token:
                post_data = {'refresh_token': refresh_token}
            else:
                raise AuthorizationError

        refresh_res = requests.post(REFRESH_URI, json=post_data)
        try:
            refresh_data = refresh_res.json()
            assert 'access_token' in refresh_data.keys()
        except:
            raise AuthorizationError

        refresh_data['expires_on'] = int(time.time()) + refresh_data['expires_in']
        if auth_code:
            refresh_data['auth_code'] = auth_code

        with open(CREDS_PATH, 'w+') as f:
            try:
                creds = json.load(f)
            except:
                creds = {}
            creds['auth_code'] = auth_code
            creds.update(refresh_data)
            json.dump(creds, f)
        return refresh_data


    def _handle_request(self, req, endpoint, kwargs):
        try:
            if endpoint.startswith('/'):
                endpoint = endpoint[1:]

            res = req(API_URL + endpoint, **kwargs)
            data = res.json()
        except:
            raise Exception('Invalid request')
    
        return data


    def request(self, endpoint, method='GET', headers={}, json=None, data=None):
        if self.is_expired():
            self.refresh()

        access_token = self.get_credentials().get('access_token')
        if not access_token:
            raise Exception('Please authenticate the CLI (spotify auth login)')

        headers['Authorization'] = 'Bearer ' + access_token
        if method == 'GET':
            req = requests.get
        elif method == 'POST':
            req = requests.post
        else:
            raise Exception('Please use a valid method')

        request_kwargs = {
            'headers': headers,
            'json': json,
            'data': data
        }
        data = self._handle_request(req, endpoint, request_kwargs)

        if 'expired' in data.get('error', {}).get('message', ''):
            self.refresh()
            access_token = self.get_credentials().get('access_token')
            data = self._handle_request(req, endpoint, request_kwargs)

        return data
