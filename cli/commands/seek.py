import click

from ..utils import Spotify
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.argument(
    'mode', type=click.Choice(['to', 'forward', 'rewind', 'percent'], case_sensitive=False),
    metavar='<mode>'
)
@click.argument(
    'position', type=float,
    metavar='<position>'
)
def seek(mode, position):
    """Seek to time (in seconds) in current track.

    Example: spotify seek to 70
    """
    if mode == 'to':
        new_position_ms = int(position * 1000)
    else:
        from cli.commands.status import status
        status_data = status.callback(raw=True, verbose=-1)
        progress_ms = status_data.get('progress_ms')
        duration_ms = status_data.get('item').get('duration_ms')
        if mode == 'forward':
            new_position_ms = min(int(progress_ms + position * 1000), duration_ms)
        elif mode == 'rewind':
            new_position_ms = max(int(progress_ms - position * 1000), 0)
        elif mode == 'percent':
            new_position_ms = int((position / 100.0) * duration_ms)

    Spotify.request(
        'me/player/seek?position_ms={}'.format(new_position_ms),
        method='PUT',
        handle_errs={404: NoPlaybackError}
    )
    click.echo('Position set to {} ms.'.format(new_position_ms))
    return
