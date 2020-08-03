import click

from cli.utils import Spotify
from cli.utils.functions import retry
from cli.utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', type=str,
    help='Search for a track to play.',
    metavar='<keyword>'
)
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
@click.option(
    '-s', '--shuffle',
    type=click.Choice(['on', 'off'], case_sensitive=False),
    help='Turn shuffle on or off.'
)
@click.option(
    '-r', '--repeat',
    type=click.Choice(['all', 'track', 'off'], case_sensitive=False),
    help='Turn repeat on (all/track) or off.'
)
def play(verbose=0, quiet=False, shuffle=None, repeat=None, track=None, _request_kwargs={}):
    """Resume playback."""
    is_search = False
    keywords = ''
    requests = []
    if track:
        is_search = True
        search_type = 'track'
        keywords = track

    if is_search:
        import urllib.parse as ul
        pager = Spotify.Pager(
            'search',
            params={
                'q': ul.quote_plus(keywords),
                'type': search_type,
            },
            content_callback=lambda c: c[search_type+'s'],
        )
        if len(pager.content) == 0:
            click.echo('No results found for "{}"'.format(keywords), err=True)
            return
        
        item = pager.content['items'][0]
        if search_type == 'track':
            _request_kwargs = {'data': {
                'context_uri': item['album']['uri'],
                'offset': {
                    'uri': item['uri'],
                },
            }}
        else:
            raise FeatureInDevelopment


    if shuffle:
        from cli.commands.shuffle import shuffle as shuffle_cmd
        requests.append(
            shuffle_cmd.callback(shuffle, _create_request=True)
        )
        verbose = max(verbose, 1)

    if repeat:
        from cli.commands.repeat import repeat as repeat_cmd
        requests.append(
            repeat_cmd.callback(repeat, _create_request=True)
        )
        verbose = max(verbose, 1)

    Spotify.multirequest(requests)
    Spotify.request(
        'me/player/play', method='PUT',
        ignore_errs=[403],
        handle_errs={404: NoPlaybackError},
        **_request_kwargs
    )

    if not quiet:
        from cli.commands.status import status
        retry(
            status.callback,
            retries=3, sleep=0.5, catch=TypeError,
            verbose=verbose, _override={'is_playing': True}
        )

    return
