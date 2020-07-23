import os
import json
import time

import click

from cli.utils import Spotify
from cli.utils.constants import *
from cli.utils.functions import build_auth_url


@click.command()
def login():
    """Authorize spotify-cli to access the Spotify API."""
    # select scopes
    import webbrowser
    from PyInquirer import prompt
    choices = filter(lambda x: x['value'] != 'default', AUTH_SCOPES_MAPPING)
    click.echo('By default, spotify-cli will enable reading & modifying the playback state.\n')
    questions = [{
        'type': 'checkbox',
        'name': 'scopes',
        'message': 'Please select which additional features you want to authorize.',
        'choices': choices,
    }]
    choice = prompt(questions)
    additional_scopes = choice.get('scopes')
    url = build_auth_url(additional_scopes)

    # handle auth and save credentials
    webbrowser.open(url)
    print('\nGo to the following link in your browser:\n\n\t{}\n'.format(url))
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
@click.group(
    options_metavar='[<options>]',
    subcommand_metavar='<command>'
)
def auth():
    """Manage user authentication for spotify-cli."""
    pass

auth.add_command(login)
auth.add_command(status)
