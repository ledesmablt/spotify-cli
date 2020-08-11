import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.exceptions import *
from ..utils.functions import cut_string


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'save_type', flag_value='track', default=True,
    help='(default) Save the current track to your Liked Songs.'
)
@click.option(
    '--album', 'save_type', flag_value='album',
    help='Save the current album to your library.'
)
@click.option(
    '--artist', 'save_type', flag_value='artist',
    help='Follow the current artist.'
)
@click.option(
    '--playlist', 'save_type', flag_value='playlist',
    help='Follow the current playlist.'
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
def save(keyword, save_type, yes, quiet=False):
    """Save a track, album, artist, or playlist.

    Example: Use 'spotify save .' to save the current track.
    """
    keyword = ' '.join(keyword)
    if keyword == '.':
        from cli.commands.status import status
        playback_data = status.callback(_return_parsed=True)
        music = playback_data['music']
    else:
        import urllib.parse as ul
        pager = Spotify.Pager(
            'search',
            params={
                'q': ul.quote_plus(keyword),
                'type': save_type,
            },
            content_callback=lambda c: c[save_type+'s'],
        )
        if len(pager.content['items']) == 0:
            click.echo('No results found for "{}"'.format(keywords), err=True)
            return

        music = pager.content['items'][0]

    # parse command and playback context
    if keyword == '.' and save_type != 'playlist':
        music = music[save_type]

    if save_type in ['track', 'album']:
        id_str = music['id']
        name = '{} - {}'.format(
            cut_string(music['name'], 50),
            cut_string(
                ', '.join(parse_artists(music['artists'])['names']), 30
            ),
        )

    elif save_type == 'artist':
        id_str = music['id']
        name = music['name']

    elif save_type == 'playlist':
        # playlist and radio are both type 'playlist'
        if keyword == '.':
            if music['context']['type'] != 'playlist':
                click.echo(
                    'Error: Current session is not a playlist.',
                    err=True
                )
                return

            id_str = music['context']['id']
            name = Spotify.request('playlists/' + id_str)['name']
        else:
            id_str = music['id']
            name = music['name']

    # format endpoint
    data = None
    if save_type in ['track', 'album']:
        endpoint = 'me/{}s?ids={}'.format(save_type, id_str)
        message = 'Saved {} - {} to library.'.format(save_type, name)

    elif save_type == 'artist':
        endpoint = 'me/following?type=artist&ids={}'.format(id_str)
        message = 'Following {} - {}.'.format(save_type, name)

    elif save_type == 'playlist':
        endpoint = 'playlists/{}/followers'.format(id_str)
        message = 'Following {} - {}.'.format(save_type, name)
        data = {'public': True}

    if not yes:
        click.confirm(
            name + '\nSave this {} to your library?'.format(save_type),
            default=True, abort=True
        )

    Spotify.request(
        endpoint, method='PUT', data=data,
        handle_errs={
            403: (AuthScopeError, {'required_scope_key': 'user-modify'})
        }
    )
    click.echo(message)
    return
