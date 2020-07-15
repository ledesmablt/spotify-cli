import click

from utils import Spotify
from utils.exceptions import *


@click.command(name='list')
@click.option('-v', '--verbose', count=True)
@click.option('--raw', is_flag=True)
def _list(verbose=0, raw=False):
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


@click.command()
@click.option('-n', '--name', type=str)
@click.option('--play', is_flag=True)
def switch(name='', play=False):
    if not name:
        name = ''
        # interactive prompt
        pass

    devices_list = _list.callback(verbose=-1, raw=True)['devices']
    matched_devices = [x for x in devices_list if name.lower() in x['name'].lower()]
    num_matched = len(matched_devices)
    if num_matched != 1:
        if num_matched == 0:
            click.echo(
                f'"{name}" not found. Please select a valid device.',
                err=True
            )
        else:
            click.echo(
                f'{num_matched} devices matched "{name}". Please select the device to activate below.'
            )

        # interactive prompt
        return


    to_activate = matched_devices[0]
    post_data = {
        'device_ids': [to_activate['id']],
        'play': play
    }
    Spotify.request('me/player', method='PUT', data=post_data)
    print(f"Switched to {to_activate['name']}")

    return
        

# CLI group
@click.group()
def devices():
    pass

devices.add_command(_list)
devices.add_command(switch)
