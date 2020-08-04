import click

from cli.utils import Spotify
from cli.utils.parsers import *
from cli.utils.functions import cut_string
from cli.utils.exceptions import AuthScopeError, FeatureInDevelopment


@click.command(options_metavar='[<options>]')
@click.option(
    '-y', '--yes', is_flag=True,
    help='Skip the confirmation prompt.'
)
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
@click.argument('keyword', type=str, metavar='<keyword>')
def queue(keyword, yes=False, verbose=0, quiet=False):
    """Add a track to your queue.

    Example: Use 'spotify queue .' to add the current track.
    """
    if keyword == '.':
        from cli.commands.status import status
        playback_data = status.callback(_return_parsed=True)
        track = playback_data['music']['track']
    else:
        import urllib.parse as ul
        pager = Spotify.Pager(
            'search',
            params={
                'q': ul.quote_plus(keyword),
                'type': 'track',
            },
            content_callback=lambda c: c['tracks'],
        )
        if len(pager.content['items']) == 0:
            click.echo('No results found for "{}"'.format(keywords), err=True)
            return

        track = pager.content['items'][0]


    # parse command and playback context
    display_str = '{} - {}'.format(
        cut_string(track['name'], 50),
        cut_string(', '.join(parse_artists(track['artists'])['names']), 30)
    )

    # handle confirmation & request
    if not yes:
        click.confirm(
            display_str + '\nAdd this track to the queue?',
            default=True, abort=True
        )

    endpoint = 'me/player/queue?uri=' + track['uri']
    Spotify.request(
        endpoint, method='POST',
        handle_errs={}
    )
    if not quiet:
        if not yes:
            click.echo('Track added to the queue.')
        else:
            click.echo('Added track to queue:\n' + display_str)

    return
