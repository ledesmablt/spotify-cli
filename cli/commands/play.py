import click

from ..utils import Spotify
from ..utils.functions import retry
from ..utils.exceptions import *
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'play_type', flag_value='track', default=True,
    help='(default) Play a track.'
)
@click.option(
    '--album', 'play_type', flag_value='album',
    help='Play an album'
)
@click.option(
    '--playlist', 'play_type', flag_value='playlist',
    help='Play a playlist'
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
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
@click.argument(
    'keyword', type=str, metavar='[<keyword>]',
    required=False, nargs=-1
)
def play(
    keyword=None, play_type='track', verbose=0, quiet=False,
    shuffle=None, repeat=None, *args, **kwargs
):
    """Resume playback or search for a track/album/playlist to play.

    Example: Use 'spotify play <keyword>' to search for and
    play a track matching <keyword>.
    """
    from cli.commands.shuffle import shuffle as shuffle_cmd

    requests = []
    keyword = ' '.join(keyword)
    if keyword:
        import urllib.parse as ul
        pager = Spotify.Pager(
            'search',
            params={
                'q': ul.quote_plus(keyword),
                'type': play_type,
            },
            content_callback=lambda c: c[play_type+'s'],
        )
        if len(pager.content['items']) == 0:
            click.echo('No results found for "{}"'.format(keyword), err=True)
            return

        item = pager.content['items'][0]
        if play_type == 'track':
            kwargs['data'] = {
                'context_uri': item['album']['uri'],
                'offset': {
                    'uri': item['uri'],
                },
            }
        elif play_type in ['album', 'playlist']:
            kwargs['data'] = {
                'context_uri': item['uri'],
            }
            if not shuffle:
                # override shuffle state if not explicitly stated
                requests.append(
                    shuffle_cmd.callback(shuffle, _create_request=True)
                )

    if shuffle:
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
        *args, **kwargs
    )

    if not quiet:
        from cli.commands.status import status
        retry(
            status.callback,
            retries=3, sleep=0.5, catch=TypeError,
            verbose=verbose, _override={'is_playing': True}
        )

    return
