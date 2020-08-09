import click

from ..utils import Spotify
from ..utils.exceptions import NoPlaybackError


@click.command(options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
@click.argument(
    'mode', type=click.Choice(['all', 'track', 'off'], case_sensitive=False)
)
def repeat(mode, verbose=0, quiet=False, _create_request=False):
    """Turn repeat on (all/track) or off."""
    state_map = {
        'all': 'context',
        'track': 'track',
        'off': 'off'
    }
    request = {
        'endpoint': 'me/player/repeat?state={}'.format(state_map[mode]),
        'method': 'PUT',
        'handle_errs': {404: NoPlaybackError},
    }
    if _create_request:
        return request

    Spotify.request(**request)
    if quiet:
        return

    if verbose == 0:
        if mode == 'off':
            click.echo('Repeat turned off.')
        elif mode == 'track':
            click.echo('Repeat set to current track.')
        elif mode == 'all':
            click.echo('Repeat set to all tracks.')
    else:
        from cli.commands.status import status
        status.callback(
            verbose=verbose,
            _override={'is_repeat': mode in ['all', 'track']}
        )

    return
