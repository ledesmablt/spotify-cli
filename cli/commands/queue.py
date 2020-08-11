import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.functions import cut_string
from ..utils.exceptions import AuthScopeError, FeatureInDevelopment


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'queue_type', flag_value='track', default=True,
    help='(default) Add a track to the queue.',
    metavar='<keyword>'
)
@click.option(
    '--album', 'queue_type', flag_value='album',
    help='Add an album to the queue.',
    metavar='<keyword>'
)
@click.option(
    '-y', '--yes', is_flag=True,
    help='Skip the confirmation prompt.'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
@click.argument(
    'keyword', type=str, metavar='<keyword>',
    nargs=-1, required=True
)
def queue(keyword, queue_type='track', yes=False, quiet=False):
    """Add a track or album to your queue.

    Example: Use 'spotify queue .' to add the current track.
    """
    keyword = ' '.join(keyword)
    if keyword == '.':
        from cli.commands.status import status
        playback_data = status.callback(_return_parsed=True)
        item = playback_data['music']['track']
    else:
        import urllib.parse as ul
        pager = Spotify.Pager(
            'search',
            params={
                'q': ul.quote_plus(keyword),
                'type': queue_type,
            },
            content_callback=lambda c: c[queue_type+'s'],
        )
        if len(pager.content['items']) == 0:
            click.echo('No results found for "{}"'.format(keywords), err=True)
            return

        item = pager.content['items'][0]

    # parse command and playback context
    display_str = '{} - {}{}'.format(
        cut_string(item['name'], 50),
        cut_string(', '.join(parse_artists(item['artists'])['names']), 30),
        '' if queue_type == 'track'
        else ' ({} tracks)'.format(item['total_tracks']),
    )

    # handle confirmation & request
    if not yes:
        click.confirm(
            display_str + '\nAdd this {} to the queue?'.format(queue_type),
            default=True, abort=True
        )

    if queue_type == 'track':
        uris = [item['uri']]
    else:
        album = Spotify.request('albums/' + item['id'])
        uris = [
            track['uri']
            for track in album['tracks']['items']
        ]

    requests = [
        {
            'endpoint': 'me/player/queue?uri=' + uri,
            'method': 'POST',
        }
        for uri in uris
    ]
    Spotify.multirequest(requests, delay_between=0.25)

    # print output
    if not quiet:
        click.echo(
            queue_type.capitalize() +
            ' added to queue' +
            ('.' if not yes else ':\n' + display_str)
        )

    return
