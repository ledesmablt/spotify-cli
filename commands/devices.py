import click

from utils import Spotify
from utils.exceptions import *


@click.command()
@click.option('-v', '--verbose', count=True)
@click.option('--raw', is_flag=True)
@click.option('-s', '--switch-to', type=str)
def devices(verbose=0, raw=False, switch_to=''):
    res = Spotify.request('me/player/devices', method='GET')
    if raw:
        if verbose >= 0:
            click.echo(res)

        return res

    if not res:
        raise NoPlaybackError

    # parsed
    devices_list = sorted(
        res['devices'],
        key=lambda x: (x['is_active'], x['type'], x['name'])
    )

    # output
    if not switch_to:
        if not verbose:
            output_list = map(
                lambda x: f"* {x['name']}" if x['is_active'] else f"  {x['name']}",
                sorted(devices_list, key=lambda x: x['name'])
            )
            click.echo('\n'.join(output_list))

        if verbose == 1:
            output_list = map(
                lambda x: f"* {x['name']} - {x['type']}" if x['is_active'] else f"  {x['name']} - {x['type']}",
                sorted(devices_list, key=lambda x: x['name'])
            )
            click.echo('\n'.join(output_list))

        return


    if not switch_to:
        switch_to = ''
        # interactive prompt
        pass

    matched_devices = [x for x in devices_list if switch_to.lower() in (x['name'] + x['type']).lower()]
    num_matched = len(matched_devices)
    if num_matched != 1:
        if num_matched == 0:
            click.echo(
                f'"{switch_to}" not found. Please select a valid device.',
                err=True
            )
        else:
            click.echo(
                f'{num_matched} devices matched "{switch_to}". Please select the device to activate below.'
            )

        # interactive prompt
        return


    to_activate = matched_devices[0]
    post_data = {
        'device_ids': [to_activate['id']],
    }
    Spotify.request('me/player', method='PUT', data=post_data)
    print(f"Switched to {to_activate['name']} - {to_activate['type']}")

    return
