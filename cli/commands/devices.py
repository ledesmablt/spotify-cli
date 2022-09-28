import beaupy
import click

from ..utils import Spotify
from ..utils.exceptions import NoPlaybackError


@click.command(options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', is_flag=True,
    help='Output more info.'
)
@click.option(
    '-s', '--switch-to', type=str,
    help='Change the currently active device.',
    metavar='<name>'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
def devices(verbose=False, switch_to='', raw=False):
    """Manage active devices.

    Only devices with an active Spotify session will be recognized.
    """
    res = Spotify.request('me/player/devices', method='GET')
    if not res.get('devices'):  # type: ignore
        raise NoPlaybackError

    if raw:
        if verbose:
            import json
            click.echo(json.dumps(res))

        return res

    # parsed
    devices_list = sorted(
        res['devices'],  # type: ignore
        key=lambda x: (x['is_active'], x['type'], x['name'])
    )
    for device in devices_list:
        device['formatted_name'] = '{} - {}'.format(
            device['name'], device['type']
        )

    # output
    if not switch_to:
        if not verbose:
            output_list = map(
                lambda x: (
                    '* ' + x['name'] if x['is_active']
                    else '  ' + x['name']
                ),
                sorted(devices_list, key=lambda x: x['name'])
            )
            click.echo('\n'.join(output_list))

        else:
            output_list = map(
                lambda x: (
                    '* ' + x['formatted_name'] if x['is_active']
                    else '  ' + x['formatted_name']
                ),
                sorted(devices_list, key=lambda x: x['formatted_name'])
            )
            click.echo('\n'.join(output_list))

        return

    # switch-to handler
    matched_devices = [
        x for x in devices_list
        if switch_to.lower() in x['formatted_name'].lower()
    ]
    num_matched = len(matched_devices)
    if num_matched != 1:
        if num_matched == 0:
            click.echo('"{}" not found.'.format(switch_to))
            message = 'Please select a valid device.\n'
            choices = devices_list
        else:
            click.echo(
                '{} devices matched "{}".'
                .format(num_matched, switch_to)
            )
            message = 'Please select the device to activate.\n'
            choices = matched_devices

        # Comprehension is more Pythonic than map() and
        # beaupy uses preprocessor instead of choice dicts
        # Also the map of lambda of sorted took me a while to decipher ;-;
        choices = sorted(choices,
                         key=lambda x: (x['is_active'], x['formatted_name']))

        # Interactive prompt
        click.echo(message)

        def name_to_display(choice: dict) -> str:
            """Replacement for 'value' in PyInquirer choice dicts."""
            name = choice['formatted_name']
            if choice['is_active']:
                return name + ' (active)'
            return name

        choice = beaupy.select(options=choices,
                               preprocessor=name_to_display)

        if choice is None:
            return

        matched_devices = [
            x for x in devices_list
            if choice['formatted_name'] == x['formatted_name']  # type: ignore
        ]

    to_activate = matched_devices[0]
    if to_activate['is_active']:
        click.echo(to_activate['formatted_name'] + ' is already active.')
        return

    post_data = {
        'device_ids': [to_activate['id']],
    }
    Spotify.request('me/player', method='PUT', data=post_data)
    print('Switched to ' + to_activate['formatted_name'])

    return
