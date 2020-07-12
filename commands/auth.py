import os
import json
import time
from uuid import uuid1

import click
import requests

from utils import Spotify
from utils.constants import AUTH_URL, CREDS_PATH 


@click.command()
def login():
    url = AUTH_URL + '&state=' + str(uuid1())
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        print('Go to the following link in your browser:\n\n\t' + url)

    auth_code = input('Enter verification code: ')
    print('\nObtaining access token...')
    Spotify.refresh(auth_code)
    print('Credentials saved to ' + CREDS_PATH)
    return


@click.command()
def status():
    user_data = Spotify.request('me', method='GET')
    try:
        print('Logged in as {}'.format(user_data['display_name']))
    except:
        print('LOGIN ERROR')
    return


# CLI group
@click.group()
def auth():
    pass

auth.add_command(login)
auth.add_command(status)
