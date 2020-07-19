import os
import json
import time
from uuid import uuid1

import click

from cli.utils import Spotify
from cli.utils.constants import AUTH_URL, CREDS_PATH 


@click.command()
def login():
    """Authorize spotify-cli to access the Spotify API."""
    url = AUTH_URL + '&state=' + str(uuid1())
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        pass
    
    print('Go to the following link in your browser:\n\n\t{}\n'.format(url))

    auth_code = input('Enter verification code: ')
    print('\nObtaining access token...')
    Spotify.refresh(auth_code)
    print('Credentials saved to {}'.format(CREDS_PATH))
    return


@click.command()
@click.option(
    '-v', '--verbose', is_flag=True,
    help='Output more info (i.e. credential storage)'
)
def status(verbose):
    """Show who's logged in."""
    user_data = Spotify.request('me', method='GET')
    click.echo('Logged in as {}'.format(user_data['display_name']))
    if verbose:
        click.echo('Credentials stored in {}'.format(CREDS_PATH))
    return


# CLI group
@click.group()
def auth():
    """Manage user authentication for spotify-cli."""
    pass

auth.add_command(login)
auth.add_command(status)
