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
    enabled_scopes = Spotify.get_config().get('auth_scopes', [])
    choices = list(filter(lambda x: x['value'] != 'default', AUTH_SCOPES_MAPPING))
    for c in choices:
        if c['value'] in enabled_scopes:
            c['name'] = '(enabled) ' + c['name']

    click.echo('By default, spotify-cli will enable reading & modifying the playback state.\n')
    choice = prompt([{
        'type': 'checkbox',
        'name': 'scopes',
        'message': 'Please select which additional features you want to authorize.',
        'choices': choices,
    }])
    if not choice:
        return

    # confirm
    additional_scopes = choice.get('scopes', [])
    click.echo(
        '\n{} features selected. This will overwite your existing credentials.'
        .format(len(additional_scopes))
    )
    confirmation = prompt([{
        'type': 'confirm',
        'name': 'confirm',
        'message': 'Proceed with these settings?',
    }])
    if not confirmation.get('confirm', False):
        click.echo('Cancelled by user')
        return

    # handle auth and save credentials
    url = build_auth_url(additional_scopes)
    webbrowser.open(url)
    click.echo('\nGo to the following link in your browser:\n\n\t{}\n'.format(url))
    auth_code = input('Enter verification code: ')
    click.echo('\nObtaining access token...')
    Spotify.refresh(auth_code)
    Spotify.update_config({'auth_scopes': additional_scopes})
    click.echo('Credentials saved to {}'.format(CREDS_PATH))
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
