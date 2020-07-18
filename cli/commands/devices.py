import click

from cli.utils import Spotify
from cli.utils.exceptions import *


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
    for device in devices_list:
        device['formatted_name'] = '{} - {}'.format(device['name'], device['type'])

    # output
    if not switch_to:
        if not verbose:
            output_list = map(
                lambda x: '* ' + x['name'] if x['is_active'] else '  ' + x['name'],
                sorted(devices_list, key=lambda x: x['name'])
            )
            click.echo('\n'.join(output_list))

        else:
            output_list = map(
                lambda x: '* ' + x['formatted_name'] if x['is_active'] else '  ' + x['formatted_name'],
                sorted(devices_list, key=lambda x: x['formatted_name'])
            )
            click.echo('\n'.join(output_list))

        return


    # switch-to handler
    matched_devices = [x for x in devices_list if switch_to.lower() in x['formatted_name'].lower()]
    num_matched = len(matched_devices)
    if num_matched != 1:
        if num_matched == 0:
            click.echo('"{}" not found.'.format(switch_to))
            message = 'Please select a valid device.\n'
            choices = devices_list
        else:
            click.echo('{} devices matched "{}".'.format(num_matched, switch_to))
            message = 'Please select the device to activate below.\n'
            choices = matched_devices

        choices = map(
            lambda x: {
                'value': x['formatted_name'],
                'name': x['formatted_name'] + ('' if not x['is_active'] else ' (active)'),
            },
            sorted(choices, key=lambda x: (x['is_active'], x['formatted_name']))
        )

        # interactive prompt
        from PyInquirer import prompt
        questions = [{
            'type': 'list',
            'name': 'formatted_name',
            'message': message,
            'choices': choices,
        }]
        choice = prompt(questions)
        if not choice:
            return

        matched_devices = [x for x in devices_list if choice['formatted_name'] == x['formatted_name']]


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