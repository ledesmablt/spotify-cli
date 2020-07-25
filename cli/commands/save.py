import click

from cli.utils import Spotify


@click.command(options_metavar='[<options>]')
@click.option('--track', 'save_type', flag_value='track', default=True)
@click.option('--album', 'save_type', flag_value='album')
@click.option('--artist', 'save_type', flag_value='artist')
@click.option('--playlist', 'save_type', flag_value='playlist')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
def save(save_type, verbose=0, quiet=False):
    """Save the current track, album, artist, or playlist."""
    from cli.commands.status import status
    playback_data = status.callback(_return_parsed=True)
    music = playback_data['music']

    # parse command and playback context
    if save_type in ['track', 'album', 'artist']:
        id_str = music[save_type]['id']
        name = music[save_type]['name']

    elif save_type == 'playlist':
        # playlist and radio are both type 'playlist'
        if music['context']['type'] != 'playlist':
            click.echo('Error: Current session is not a playlist.', err=True)
            return

        id_str = music['context']['id']
        name = Spotify.request('playlists/' + id_str)['name']


    # format endpoint
    data = None
    headers = {}
    if save_type in ['track', 'album']:
        endpoint = 'me/{}s?ids={}'.format(save_type, id_str)
        message = 'Saved {} - {} to library.'.format(save_type, name)

    elif save_type == 'artist':
        endpoint = 'me/following?type=artist&ids={}'.format(id_str)
        message = 'Following {} - {}.'.format(save_type, name)

    elif save_type == 'playlist':
        endpoint = 'playlists/{}/followers'.format(id_str)
        message = 'Following {} - {}.'.format(save_type, name)
        headers = {'Content-Type': 'application/json'}
        data = {'public': True}

    Spotify.request(endpoint, method='PUT', data=data, headers=headers)
    click.echo(message)
    return
