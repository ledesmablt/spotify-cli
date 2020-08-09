import os

# spotify API URL
API_URL = 'https://api.spotify.com/v1/'
DEFAULT_HEADERS = {
    'Content-Type': 'application/json'
}

# credential storage
HOME = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME, '.config')
CREDS_DIR = os.path.join(CONFIG_DIR, 'spotify-cli')
CREDS_PATH = os.path.join(CREDS_DIR, 'credentials.json')
CONFIG_PATH = os.path.join(CREDS_DIR, 'config.json')
for folder in [CONFIG_DIR, CREDS_DIR]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# auth
CLOUD_URI_PREFIX = 'https://asia-east2-spotify-cli-283006.cloudfunctions.net/'
REFRESH_URI = CLOUD_URI_PREFIX + 'auth-refresh'
REDIRECT_URI = CLOUD_URI_PREFIX + 'auth-redirect'
CLIENT_ID = '3e96f0ef8d6d4e0994e15bf2b168235f'

AUTH_SCOPES_MAPPING = [
    {
        'value': 'default',
        'name': 'Read & modify playback.',
        'scopes': [
           'user-read-playback-state',
           'user-modify-playback-state',
           'user-read-recently-played',
        ],
    },
    {
        'value': 'playlists-read',
        'name': 'Read user playlists.',
        'scopes': [
            'playlist-read-collaborative',
            'playlist-read-private',
        ],
    },
    {
        'value': 'playlists-modify',
        'name': 'Modify user playlists.',
        'scopes': [
            'playlist-modify-public',
            'playlist-modify-private',
        ],
    },
    {
        'value': 'user-read',
        'name': (
            'Read user library, followed artists/users, '
            'and top artists/tracks.'
        ),
        'scopes': [
            'user-top-read',
            'user-library-read',
            'user-follow-read',
        ],
    },
    {
        'value': 'user-modify',
        'name': 'Modify user library and followed artists/users.',
        'scopes': [
            'user-library-modify',
            'user-follow-modify',
        ],
    }
]
