import click

from ..utils import Spotify
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.argument(
    'position', type=int,
    metavar='<position>'
)
def seek(position):
    """Seek to time (in ms) in current track.

    Example: spotify seek 10000
    """
    Spotify.request(
        'me/player/seek?position_ms={}'.format(position),
        method='PUT',
        handle_errs={404: NoPlaybackError}
    )
    click.echo('Position set to {} ms.'.format(position))
    return
