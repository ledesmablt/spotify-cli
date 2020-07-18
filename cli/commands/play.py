import click

from cli.utils import Spotify
from cli.utils.exceptions import SpotifyAPIError


@click.command()
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', is_flag=True)
def play(verbose=0, quiet=False):
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
