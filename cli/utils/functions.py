import urllib.parse as ul
from uuid import uuid1
from datetime import timedelta

from cli.utils.constants import *


def format_duration_ms(ms):
    def _format(d):
        d = str(d)
        if len(d) == 1:
            d = '0' + d
        return d

    s = int(ms / 1000)
    if s < 60:
        return '00:{}'.format(_format(s))

    m, s = divmod(s, 60)
    return '{}:{}'.format(_format(m), _format(s))


def build_auth_url(additional_scopes=[]):
    user_scopes = ['default'] + additional_scopes
    scopes = []
    for scope in AUTH_SCOPES_MAPPING:
        if scope['value'] in user_scopes:
            scopes += scope['scopes']

    auth_url = (
        'https://accounts.spotify.com/authorize?client_id={}'
        '&response_type=code&redirect_uri={}&scope={}&state={}'
        .format(
            CLIENT_ID,
            ul.quote_plus(REDIRECT_URI),
            ul.quote_plus(" ".join(scopes)),
            uuid1()
        )
    )
    return auth_url
