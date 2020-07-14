import os
import json
import time
from uuid import uuid1

import click

from utils import Spotify
from utils.constants import AUTH_URL, CREDS_PATH 


@click.command()
def login():
    url = AUTH_URL + '&state=' + str(uuid1())
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        print(f'Go to the following link in your browser:\n\n\t{url}')

    auth_code = input('Enter verification code: ')
    print('\nObtaining access token...')
    Spotify.refresh(auth_code)
    print(f'Credentials saved to {CREDS_PATH}')
    return


@click.command()
@click.option('-v', '--verbose', is_flag=True)
def status(verbose):
    user_data = Spotify.request('me', method='GET')
    click.echo(f"Logged in as {user_data['display_name']}")
    if verbose:
        click.echo(f'Credentials stored in {CREDS_PATH}')
    return


# CLI group
@click.group()
def auth():
    pass

auth.add_command(login)
auth.add_command(status)
