import json
import requests
from flask import jsonify


REFRESH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = (
    'https://asia-east2-spotify-cli-283006.cloudfunctions.net/'
    'auth-redirect'
)
with open('credentials.json') as f:
    CREDENTIALS = json.load(f)


def main(request):
    """Handler for refreshing the user access token."""
    request_data = request.get_json()
    auth_code = request_data.get('auth_code')
    refresh_token = request_data.get('refresh_token')
    post_data = {
        'client_id': (
            request_data.get('client_id') or CREDENTIALS['client_id']
        ),
        'client_secret': (
            request_data.get('client_secret') or CREDENTIALS['client_secret']
        ),
        'redirect_uri': REDIRECT_URI,
    }
    if auth_code:
        post_data['grant_type'] = 'authorization_code'
        post_data['code'] = auth_code
    elif refresh_token:
        post_data['grant_type'] = 'refresh_token'
        post_data['refresh_token'] = refresh_token

    res = requests.post(REFRESH_URL, data=post_data)
    return jsonify(res.json())
