import click
import re

from ..utils import Spotify
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.argument(
    'position', type=str,
    metavar='<position>'
)
def seek(position):
    """Seek to time (in seconds) in current track.

    Examples: spotify seek +70s
              spotify seek -- -1m10s
              spotify seek 50%
    """
    tokens = [s for s in re.split('(%|ms|m|s|\+|\-)', position) if len(s) > 0]
    print (tokens)
    if len(tokens) > 0:
        from cli.commands.status import status
        status_data = status.callback(raw=True, verbose=-1)
        progress_ms = status_data.get('progress_ms')
        duration_ms = status_data.get('item').get('duration_ms')

        relative_factor = 0
        if tokens[0] == '+':
            relative_factor = 1
            tokens.pop(0)
        elif tokens[0] == '-':
            relative_factor = -1
            tokens.pop(0)

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
            raise InvalidInput(' Expected unit (m, s, ms or %) at the end of the input.')

        if relative_factor != 0:
            new_position_ms = progress_ms + relative_factor * new_position_ms

        new_position_ms = min(max(0, new_position_ms), duration_ms)

        Spotify.request(
            'me/player/seek?position_ms={}'.format(new_position_ms),
            method='PUT',
            handle_errs={404: NoPlaybackError}
        )
        click.echo('Position set to {} ms.'.format(new_position_ms))
    return
