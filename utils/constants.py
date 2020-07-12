import os
import urllib.parse as ul

# spotify API URL
API_URL = 'https://api.spotify.com/v1/'

# credential storage
HOME = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME, '.config')
CREDS_DIR = os.path.join(CONFIG_DIR, 'spotify-cli')
CREDS_PATH = os.path.join(CREDS_DIR, 'credentials.json')
for folder in [CONFIG_DIR, CREDS_DIR]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# auth
REFRESH_URI = 'https://asia-east2-spotify-cli-283006.cloudfunctions.net/auth-refresh'
REDIRECT_URI = 'https://asia-east2-spotify-cli-283006.cloudfunctions.net/auth-redirect'
CLIENT_ID = '3e96f0ef8d6d4e0994e15bf2b168235f'
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
    + f'?client_id={CLIENT_ID}'
    + f'&response_type=code'
    + f'&redirect_uri={ul.quote_plus(REDIRECT_URI)}'
    + f'&scope={ul.quote_plus(" ".join(AUTH_SCOPES))}'
)
