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
def previous(verbose=0, quiet=False):
    """Play the previous track in the queue."""
    Spotify.request(
        'me/player/previous', method='POST',
        handle_errs={404: NoPlaybackError}
    )
    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose)

    return
