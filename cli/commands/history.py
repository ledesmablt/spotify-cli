import click

from cli.utils import Spotify
from cli.utils.parsers import *
from cli.utils.functions import cut_string
from cli.utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '-l', '--limit', type=int, default=10,
    help='Number of tracks to show.'
)
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
def history(verbose=0, raw=False, limit=10, _return_parsed=False):
    """List your recently played tracks."""
    from tabulate import tabulate
    pager = Spotify.Pager('me/player/recently-played', limit=limit)
    if raw:
        if verbose >= 0:
            import json
            click.echo(json.dumps(pager.content))
        
        return pager.content

    headers = ['Artist', 'Track']
    table = []
    for item in pager.content['items']:
        parsed_item = parse_track_item_full(item['track'])
        table.append([
            cut_string(', '.join(parsed_item['artists']['names']), 30),
            cut_string(parsed_item['track']['name'], 50),
        ])

    if len(table) == 0:
        click.echo('No data available for recently played songs.', err=True)
        return

    click.echo(tabulate(table, headers=headers))
