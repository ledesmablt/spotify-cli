import click

from utils import Spotify
from utils.exceptions import *


@click.command(name='list')
@click.option('-v', '--verbose', count=True)
@click.option('--raw', is_flag=True)
def _list(verbose=0, raw=False):
    res = Spotify.request('me/player/devices', method='GET')
    if raw:
        click.echo(res)
        return res

    if not res:
        raise NoPlaybackError

    # parsed
    devices = sorted(
        res['devices'],
        key=lambda x: (x['is_active'], x['type'], x['name'])
    )

    # output
    if not verbose:
        output_list = map(
            lambda x: f"* {x['name']}" if x['is_active'] else f"  {x['name']}",
            sorted(devices, key=lambda x: x['name'])
        )
        click.echo('\n'.join(output_list))

    if verbose == 1:
        output_list = map(
            lambda x: f"* {x['name']} - {x['type']}" if x['is_active'] else f"  {x['name']} - {x['type']}",
            sorted(devices, key=lambda x: x['name'])
        )
        click.echo('\n'.join(output_list))

    if verbose >= 2:
        click.echo('\n'.join([
            '',
            f"Device  {data['device']['name']} ({data['device']['type']})",
            f"URL:    {music['song']['url']}"
        ]))


    return


# CLI group
@click.group()
def devices():
    pass

devices.add_command(_list)
