import os
import json

import requests

from utils.exceptions import *
from utils.constants import CREDS_PATH, REFRESH_URI, API_URL


def get_credentials():
    """Read locally stored credentials file for API authorization."""
    if not os.path.exists(CREDS_PATH):
        return {}

    with open(CREDS_PATH) as f:
        creds = json.load(f)

    return creds


def refresh(auth_code=None):
    """Refresh Spotify access token.

    Optional arguments:
    auth_code -- if supplied, pulls new access and refresh tokens.
    """
    post_data = {}
    if auth_code:
        post_data = {'auth_code': auth_code}
    else:
        refresh_token = get_credentials().get('refresh_token')
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


def _handle_request(req, endpoint, kwargs):
    try:
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        res = req(API_URL + endpoint, **kwargs)
        data = res.json()
    except:
        raise Exception('Invalid request')

    return data


def request(endpoint, method='GET', headers={}, json=None, data=None):
    """Request wrapper for Spotify API endpoints. Handles errors, authorization,
    and refreshing access if needed.
    """
    access_token = get_credentials().get('access_token')
    if not access_token:
        raise AuthorizationError

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
    data = _handle_request(req, endpoint, request_kwargs)

    if 'expired' in data.get('error', {}).get('message', ''):
        # refresh & retry if response says expired
        refresh()
        access_token = get_credentials().get('access_token')
        request_kwargs['headers']['Authorization'] = 'Bearer ' + access_token
        data = _handle_request(req, endpoint, request_kwargs)

    return data
