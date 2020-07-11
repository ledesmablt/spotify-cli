import os
import json
import urllib.parse as ul
from uuid import uuid1

import requests

# storage
HOME = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME, '.config')
CREDS_DIR = os.path.join(CONFIG_DIR, 'spotify-cli')
if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)
if not os.path.exists(CREDS_DIR):
    os.mkdir(CREDS_DIR)

CREDS_PATH = os.path.join(CREDS_DIR, 'credentials.json')

# auth
REFRESH_URI = 'https://asia-east2-spotify-cli-283006.cloudfunctions.net/auth-refresh'
REDIRECT_URI = 'https://asia-east2-spotify-cli-283006.cloudfunctions.net/auth-redirect'
AUTH_SCOPES = [
   'user-read-playback-state',
   'user-modify-playback-state',
   'user-library-modify',
   'user-top-read',
   'user-library-read',
   'user-read-recently-played',
]
AUTH_URL = (
    'https://accounts.spotify.com/authorize'
    '?client_id=3e96f0ef8d6d4e0994e15bf2b168235f'
    '&response_type=code'
    '&redirect_uri=' + ul.quote_plus(REDIRECT_URI) +
    '&scope=' + ul.quote_plus(' '.join(AUTH_SCOPES)) +
    '&state=' + str(uuid1())
)


def refresh(auth_code=None, refresh_token=None):
    post_data = {}
    if auth_code:
        post_data = {'auth_code': auth_code}
    elif refresh_token:
        post_data = {'refresh_token': refresh_token}
    else:
        raise Exception('Please supply an authorization code or refresh token.')

    refresh_res = requests.post(REFRESH_URI, json=post_data)
    try:
        refresh_data = refresh_res.json()
        assert 'access_token' in refresh_data.keys()
    except:
        raise Exception('Error in obtaining access token. Please try again.')

    return refresh_data


def login():
    try:
        import webbrowser
        webbrowser.open(AUTH_URL)
    except:
        print('Go to the following link in your browser:\n\n\t' + AUTH_URL)

    auth_code = input('Enter verification code: ')
    print('\nObtaining access token...')
    refresh_json = refresh(auth_code)
    with open(CREDS_PATH, 'w+') as f:
        try:
            creds = json.load(f)
        except:
            creds = {}
        creds['auth_code'] = auth_code
        creds.update(refresh_json)
        json.dump(creds, f)

    print('Credentials saved to ' + CREDS_PATH)
    return


if __name__ == '__main__':
    # test login and refresh
    login()
    with open(CREDS_PATH) as f:
        creds = json.load(f)
    refresh(refresh_token=creds['refresh_token'])
