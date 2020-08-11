import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.functions import cut_string
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '-l', '--limit', type=int, default=10,
    help='Number of tracks to show.',
    metavar='<int>'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
def history(raw=False, limit=10, _return_parsed=False):
    """List your recently played tracks."""
    from tabulate import tabulate
    from datetime import datetime
    pager = Spotify.Pager('me/player/recently-played', limit=limit)
    if raw:
        import json
        click.echo(json.dumps(pager.content))
        return pager.content

    headers = ['Last played', 'Artist', 'Track']
    current_time = datetime.utcnow()

    table = []
    timediffs = set()
    for i, item in enumerate(pager.content['items']):
        parsed_item = parse_track_item_full(item['track'])
        row_dict = {
            'Artist': cut_string(
                ', '.join(parsed_item['artists']['names']), 30
            ),
            'Track': cut_string(parsed_item['track']['name'], 50),
        }

        # last played parsing
        try:
            played_at = datetime.strptime(
                item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        except ValueError:
            played_at = datetime.strptime(
                item['played_at'], '%Y-%m-%dT%H:%M:%SZ'
            )

        timediff = current_time - played_at
        timediff_hours = int(timediff.seconds / 3600)
        if timediff.days >= 1:
            timediff_str = 'Yesterday'
        elif timediff_hours >= 1:
            timediff_str = '{} {} ago'.format(
                timediff_hours, 'hours' if timediff_hours > 1 else 'hour'
            )
        else:
            timediff_str = 'A few minutes ago'

        if timediff_str in timediffs:
            timediff_str = ''
        else:
            timediffs.add(timediff_str)

        row_dict['Last played'] = timediff_str
        row = [row_dict[h] for h in headers]
        table.append(row)

    if len(table) == 0:
        click.echo('No data available for recently played tracks.', err=True)
        return

    click.echo(tabulate(table, headers=headers))
