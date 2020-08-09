import click

from ..utils import Spotify
from ..utils.exceptions import AuthScopeError


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'browse_type', flag_value='track', default=True,
    help='(default) Open the current track in your browser.'
)
@click.option(
    '--album', 'browse_type', flag_value='album',
    help='Open the current album in your browser.'
)
@click.option(
    '--artist', 'browse_type', flag_value='artist',
    help='Open the current artist in your browser.'
)
@click.option(
    '--playlist', 'browse_type', flag_value='playlist',
    help='Open the current playlist in your browser.'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
def browse(browse_type, verbose=0, quiet=False):
    """Open the current track, album, artist, or playlist in the browser.

    Specify one of the above options to change what to browse (default: track).
    """
    import webbrowser
    from cli.commands.status import status
    playback_data = status.callback(_return_parsed=True)
    music = playback_data['music']

    # parse command and playback context
    if browse_type in ['track', 'album', 'artist']:
        url = music[browse_type]['url']
        name = music[browse_type]['name']
        if browse_type != 'artist':
            name = '"{}" by {}'.format(name, music['artist']['name'])

    elif browse_type == 'playlist':
        # playlist and radio are both type 'playlist'
        if music['context']['type'] != 'playlist':
            click.echo('Error: Current session is not a playlist.', err=True)
            return

        url = music['context']['url']
        id_str = music['context']['id']
        name = Spotify.request('playlists/' + id_str)['name']

    if not quiet:
        click.echo(
            '{} - {}\n'
            '{}'
            .format(browse_type.title(), name, url)
        )

    webbrowser.open(url)
    return
