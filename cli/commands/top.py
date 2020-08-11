import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.functions import cut_string
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '--tracks', 'top_type', flag_value='tracks', default=True,
    help='(default) List your top tracks.'
)
@click.option(
    '--artists', 'top_type', flag_value='artists',
    help='List your top artists.'
)
@click.option(
    '-t', '--time',
    default='medium',
    type=click.Choice(['short', 'medium', 'long'], case_sensitive=False),
    help=(
        'Specify the timeframe for your top '
        'tracks/artists (default: medium).'
    ),
    metavar='<int>'
)
@click.option(
    '-l', '--limit', type=int, default=10,
    help='Number of items to show.'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
def top(top_type, time, raw=False, limit=10, _return_parsed=False):
    """List your top tracks or artists."""
    from tabulate import tabulate
    pager = Spotify.Pager(
        'me/top/{}'.format(top_type),
        limit=limit,
        params={'time_range': time+'_term'}
    )
    if raw:
        import json
        click.echo(json.dumps(pager.content))
        return pager.content

    if top_type == 'tracks':
        headers = ['#', 'Track', 'Artist']
    elif top_type == 'artists':
        headers = ['#', 'Artist']

    table = []
    for i, item in enumerate(pager.content['items']):
        if top_type == 'tracks':
            parsed_item = parse_track_item_full(item)
            row_dict = {
                '#': i+1,
                'Artist': cut_string(
                    ', '.join(parsed_item['artists']['names']), 30
                ),
                'Track': cut_string(parsed_item['track']['name'], 50),
            }
        elif top_type == 'artists':
            row_dict = {
                '#': i+1,
                'Artist': cut_string(item['name'], 50),
            }

        row = [row_dict[h] for h in headers]
        table.append(row)

    if len(table) == 0:
        click.echo('No data available for top {}.'.format(top_type), err=True)
        return

    click.echo(tabulate(table, headers=headers))
