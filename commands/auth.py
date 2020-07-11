import os
import json
import urllib.parse as ul
from uuid import uuid1

import requests

# storage
HOME = os.path.expanduser('~')
CREDS_DIR = os.path.join(HOME, '.config')
if not os.path.exists(CREDS_DIR):
    os.mkdir(CREDS_DIR)

CREDS_PATH = os.path.join(CREDS_DIR, 'spotify-cli-credentials.json')

# auth
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


def login():
    try:
        import webbrowser
        webbrowser.open(AUTH_URL)
    except:
        print('Go to the following link in your browser:\n\n\t' + AUTH_URL)

    auth_code = input('Enter verification code: ')
    with open(CREDS_PATH, 'w+') as f:
        try:
            creds = json.load(f)
        except:
            creds = {}
        creds['auth_code'] = auth_code
        json.dump(creds, f)

    print('\n\nCredentials saved to ' + CREDS_PATH)
    return


if __name__ == '__main__':
    login()
