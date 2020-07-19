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
    try:
        Spotify.request('me/player/play', method='PUT')
    except SpotifyAPIError as e:
        if e.status == 403:
            pass
        else:
            raise e

    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose, override={'is_playing': True})


    return
