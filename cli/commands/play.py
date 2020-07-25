import click

from cli.utils import Spotify
from cli.utils.exceptions import SpotifyAPIError


@click.command(options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
def play(verbose=0, quiet=False):
    """Resume playback."""
    Spotify.request('me/player/play', method='PUT', ignore_errs=[403])

    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose, override={'is_playing': True})


    return
