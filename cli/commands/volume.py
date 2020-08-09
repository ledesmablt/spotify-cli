import click

from ..utils import Spotify
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.argument(
    'mode', type=click.Choice(['to', 'up', 'down'], case_sensitive=False),
    metavar='<mode>'
)
@click.argument(
    'amount', type=int,
    metavar='<amount>'
)
def volume(mode, amount):
    """Control the active device's volume level (0-100).

    Example: spotify volume to 50
    """
    if mode == 'to':
        new_volume = amount
    else:
        from cli.commands.status import status
        device = status.callback(raw=True, verbose=-1).get('device')
        current_volume = device['volume_percent']

        if mode == 'up':
            increment = amount
        elif mode == 'down':
            increment = - amount

        new_volume = current_volume + increment
        if new_volume > 100:
            new_volume = 100
        elif new_volume < 0:
            new_volume = 0

    Spotify.request(
        'me/player/volume?volume_percent={}'.format(new_volume),
        method='PUT',
        handle_errs={403: DeviceOperationRestricted}
    )
    click.echo('Volume set to {}%'.format(new_volume))
    return
