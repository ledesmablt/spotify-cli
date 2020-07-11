import os
import json
import time
import urllib.parse as ul
from uuid import uuid1

import requests
import click


# storage
HOME = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME, '.config')
CREDS_DIR = os.path.join(CONFIG_DIR, 'spotify-cli')
CREDS_PATH = os.path.join(CREDS_DIR, 'credentials.json')
for folder in [CONFIG_DIR, CREDS_DIR]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# auth
CLIENT_ID = '3e96f0ef8d6d4e0994e15bf2b168235f'
AUTH_STATUS_URL = 'https://api.spotify.com/v1/me'
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
    '?client_id=' + CLIENT_ID +
    '&response_type=code'
    '&redirect_uri=' + ul.quote_plus(REDIRECT_URI) +
    '&scope=' + ul.quote_plus(' '.join(AUTH_SCOPES)) +
    '&state=' + str(uuid1())
)


def get_credentials():
    if not os.path.exists(CREDS_PATH):
        return {}

    with open(CREDS_PATH) as f:
        creds = json.load(f)

    return creds


def _is_expired():
    creds = get_credentials()
    return int(time.time()) > creds['expires_on']


def refresh(auth_code=None):
    post_data = {}
    if auth_code:
        post_data = {'auth_code': auth_code}
    else:
        refresh_token = get_credentials().get('refresh_token')
        if refresh_token:
            post_data = {'refresh_token': refresh_token}
        else:
            raise Exception('Please supply an authorization code or refresh token.')

    refresh_res = requests.post(REFRESH_URI, json=post_data)
    try:
        refresh_data = refresh_res.json()
        assert 'access_token' in refresh_data.keys()
    except:
        raise Exception('Error in obtaining access token. Please try again.')

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


@click.command()
def login():
    try:
        import webbrowser
        webbrowser.open(AUTH_URL)
    except:
        print('Go to the following link in your browser:\n\n\t' + AUTH_URL)

    auth_code = input('Enter verification code: ')
    print('\nObtaining access token...')
    refresh(auth_code)
    print('Credentials saved to ' + CREDS_PATH)
    return


@click.command()
def status():
    creds = get_credentials()
    if _is_expired():
        refresh()
        creds = get_credentials()

    headers = {'Authorization': 'Bearer ' + creds['access_token']}
    res = requests.get(AUTH_STATUS_URL, headers=headers)
    user_data = res.json()
    try:
        print('Logged in as {}'.format(user_data['display_name']))
    except:
        print('LOGIN ERROR')
        print(user_data)
    return


# CLI group
@click.group()
def auth():
    pass

auth.add_command(login)
auth.add_command(status)


if __name__ == '__main__':
    # test login and refresh
    login()
    status()
