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
def toggle(verbose=0, quiet=False, raw=False):
    """Resume any paused playback, or pause it if already running."""

    res = Spotify.request('me/player', method='GET')
    if not res:
        raise NoPlaybackError

    if res['is_playing']:
        Spotify.request(
            'me/player/pause', method='PUT',
            ignore_errs=[403],
            handle_errs={404: NoPlaybackError}
        )
        if not quiet:
            from cli.commands.status import status
            status.callback(verbose=verbose, _override={'is_playing': False})
    else:
        Spotify.request(
            'me/player/play', method='PUT',
            ignore_errs=[403],
            handle_errs={404: NoPlaybackError}
        )

        if not quiet:
            from cli.commands.status import status
            status.callback(verbose=verbose, _override={'is_playing': True})

    return
