import click

from cli.utils import Spotify
from cli.utils.parsers import *
from cli.utils.functions import cut_string
from cli.utils.exceptions import *


all_types = 'album,artist,playlist,track'


@click.command(options_metavar='[<options>]')
@click.option(
    '-t', '--type', 'search_type', default='track',
    type=click.Choice(['artist', 'track', 'playlist', 'album'], case_sensitive=False),
    help='Types of items to search (default: track)'
)
@click.option(
    '--library', is_flag=True,
    help='Limit search results to your library.'
)
@click.option(
    '-l', '--limit', type=int, default=10,
    help='Number of items to show.'
)
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
@click.argument(
    'keywords', type=str, metavar='<keywords>'
)
def search(keywords, search_type='all', library=False, verbose=0, raw=False, limit=10, _return_parsed=False):
    """Search for any Spotify content."""
    import urllib.parse as ul
    from tabulate import tabulate

    pager = Spotify.Pager(
        'search',
        limit=limit,
        params={
            'q': ul.quote_plus(keywords),
            'type': search_type,
        },
        content_callback=lambda c: c[search_type+'s'],
    )
    if raw:
        if verbose >= 0:
            import json
            click.echo(json.dumps(pager.content))
        
        return pager.content


    if search_type == 'track':
        headers = ['Track', 'Artist']
        def _parse(item, index):
            item = parse_track_item_full(item)
            return {
                'Track': cut_string(item['track']['name'], 50),
                'Artist': cut_string(', '.join(item['artists']['names']), 30),
                'uri': item['track']['uri'],
                '#': index,
            }
    else:
        raise FeatureInDevelopment
        

    headers.insert(0, '#')
    end = False
    click.echo(
        '\nSearch results for "{}"'
        .format(keywords, int(pager.offset / pager.limit) + 1)
    )
    while not end:
        table = []
        parsed_content = []
        for i, item in enumerate(pager.content['items']):
            parsed_item = _parse(item, i)
            parsed_content.append(parsed_item)
            row = [parsed_item[h] for h in headers]
            table.append(row)

        if len(table) == 0:
            click.echo('No data available for your search query.', err=True)
            return

        click.echo('\n', nl=False)
        click.echo(tabulate(table, headers=headers))
        response = click.prompt(
            '\nActions:\n'
            '[n]ext/[b]ack\n[p]lay/[q]ueue/[s]ave #[,...]\n'
            '[a]dd to playlist #[,...] <playlist>\n'
        ).lower()

        cmd = response.split(' ')[0]
        if cmd == 'n':
            pager.next()
        elif cmd == 'b':
            pager.previous()
        else:
            raise FeatureInDevelopment

    return
