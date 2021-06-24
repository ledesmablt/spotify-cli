import click
import re

from ..utils import Spotify
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '-f', '--forward', is_flag=True,
    help='Increment playback position'
)
@click.option(
    '-r', '--reverse', is_flag=True,
    help='Decrement playback position'
)
@click.argument(
    'position', type=str,
    metavar='<position>'
)
def seek(forward, reverse, position):
    """Seek to time (default unit: seconds) in the current track.

    \b
    Examples:
    spotify seek -f 50        # increment playback position by 50s
    spotify seek -r 1m10s     # decrement playback position by 1m10s
    spotify seek 50%          # set playback position to half the track duration
    spotify seek 2m           # set playback position to 2 minutes into the track
    """
    tokens = [s for s in re.split('(%|ms|m|s)', position) if len(s) > 0]
    relative_factor = 0
    if reverse:
        relative_factor = -1
    if forward:
        relative_factor = 1
    if len(tokens) > 0:
        from cli.commands.status import status
        status_data = status.callback(raw=True, verbose=-1)
        progress_ms = status_data.get('progress_ms')
        duration_ms = status_data.get('item').get('duration_ms')

        expect_unit = False
        new_position_ms = 0

        for t in tokens:
            if not expect_unit:
                try:
                    value = float(t)
                    expect_unit = True
                except:
                    raise InvalidInput(' Expected number but can\'t convert {} to number.'.format(t))
            else:
                if t == "ms":
                    new_position_ms += int(value)
                elif t == "s":
                    new_position_ms += int(value * 1000)
                elif t == "m":
                    new_position_ms += int(value * 60000)
                elif t == "%":
                    new_position_ms += int((value / 100.0) * duration_ms)
                else:
                    raise InvalidInput(' Expected unit (m, s, ms or %) but got {}.'.format(t))
                expect_unit = False
                value = None
        if value is not None:
            new_position_ms += int(value * 1000)

        if relative_factor != 0:
            new_position_ms = progress_ms + relative_factor * new_position_ms

        new_position_ms = min(max(0, new_position_ms), duration_ms)

        Spotify.request(
            'me/player/seek?position_ms={}'.format(new_position_ms),
            method='PUT',
            handle_errs={404: NoPlaybackError}
        )

        position_str = ""
        if new_position_ms >= 60000:
            position_str += "{}m".format(new_position_ms // 60000)
        position_str += "{}s".format((new_position_ms // 1000) % 60)
        click.echo('Position set to {}.'.format(position_str))
    return
