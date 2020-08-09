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
    'mode', type=click.Choice(['on', 'off'], case_sensitive=False)
)
def shuffle(mode, verbose=0, quiet=False, _create_request=False):
    """Turn shuffle on or off."""
    request = {
        'endpoint': (
            'me/player/shuffle?state={}'
            .format('true' if mode == 'on' else 'false')
        ),
        'method': 'PUT',
        'handle_errs': {404: NoPlaybackError},
    }
    if _create_request:
        return request

    Spotify.request(**request)
    if quiet:
        return

    if verbose == 0:
        click.echo('Shuffle turned {}.'.format(mode))
    else:
        from cli.commands.status import status
        status.callback(
            verbose=verbose,
            _override={'is_shuffle': mode == 'on'}
        )

    return
