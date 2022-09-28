import webbrowser
from typing import Optional

import beaupy
import click

from ..utils import Spotify
from ..utils.constants import *
from ..utils.functions import build_auth_url


@click.command(options_metavar='[<options>]')
@click.option(
    '--client-id', type=str, metavar='<str>', default='',
    help=(
        'When provided, authenticates the CLI using your own application ID '
        'and secret (helps avoid API rate limiting issues).'
    )
)
@click.option(
    '--client-secret', type=str, metavar='<str>', default='',
    help='Required if --client-id is provided.'
)
def login(client_id='', client_secret=''):
    """Authorize spotify-cli to access the Spotify API."""
    # verify both creds are provided
    if client_id or client_secret:
        if client_id and client_secret:
            click.echo(
                'Authenticating with provided Client ID and secret.\n'
                'Please ensure that the URL below is listed as a valid '
                'redirect URI in your Spotify application:\n\n{}\n'
                .format(REDIRECT_URI)
            )
        else:
            click.echo(
                'Please provide both the Client ID and secret.',
                err=True
            )
            return

    config = Spotify.get_config()
    if config.get('client_id') and not client_id:
        reuse_creds = click.confirm(
            'You used a custom Client ID and secret to authenticate last time. '
            'Use these again?\n'
            '(Type "n" to revert to the default ID and secret)',
            default=True,
        )
        if not reuse_creds:
            client_id = ''
            client_secret = ''
            click.echo('Removing custom client ID and secret.\n')
        else:
            client_id = config.get('client_id')
            client_secret = config.get('client_secret')

    Spotify.update_config({
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # Select scopes
    
    # The strings are values for the 'name' key in respective auth scope
    enabled_scopes: list[str] = Spotify.get_config().get('auth_scopes', [])

    click.echo(
        'By default, spotify-cli will enable reading & '
        'modifying the playback state.\n'
    )
    
    click.echo(
        'Please select which additional features '
        'you want to authorize.'
    )
    
    # Determine which choices to prompt
    choices = []
    ticked = []
    index = 0
    for scope in AUTH_SCOPES_MAPPING:
        # Ignore the default scope
        if scope['value'] != 'default':
            choices.append(scope['name'])
            if scope['name'] in enabled_scopes:
                ticked.append(index)
            index += 1

    # Prompt users to choose additional scopes
    additional_scopes = beaupy.select_multiple(options=choices,
                                               ticked_indices=ticked)
    
    # UPDATED: Stopped choosing zero from doing nothing
    # User should be able to set their preference to no additional features
    # Instead, do nothing if there's no change in chosen options
    # set() casting necessary because scopes can be read in a different order
    if set(additional_scopes) == set(enabled_scopes):
        click.echo('No change in existing credentials.')
        return

    # Confirm
    click.echo(
        '\n{} features selected. This will overwite your existing credentials.'
        .format(len(additional_scopes))
    )
    click.confirm('Proceed with these settings?', default=True, abort=True)

    # handle auth and save credentials
    url = build_auth_url(additional_scopes, client_id)  # type: ignore
    webbrowser.open(url)
    click.echo(
        '\nGo to the following link in your browser:\n\n\t{}\n'
        .format(url)
    )
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
    click.echo('Logged in as {}'.format(
        user_data['display_name']))  # type: ignore
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
