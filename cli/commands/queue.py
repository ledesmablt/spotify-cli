import click

from cli.utils import Spotify
from cli.utils.exceptions import AuthScopeError, FeatureInDevelopment


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'queue_type', flag_value='track', default=True,
    help='(default) Add track <name> to the queue.'
)
@click.option(
    '--album', 'queue_type', flag_value='album',
    help='Add album <name> to the queue.'
)
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
@click.argument('name', type=str, metavar='<name>')
def queue(name, queue_type='track', yes=False, verbose=0, quiet=False):
    """Add a track or album to your queue.

    Example: Use 'spotify queue .' to add the current track.
    """
    if name == '.':
        from cli.commands.status import status
        playback_data = status.callback(_return_parsed=True)
        music = playback_data['music']
    else:
        raise FeatureInDevelopment

    # parse command and playback context
    uri = music[queue_type]['uri']
    name = music[queue_type]['name']
    total_tracks_str = (
        '' if queue_type == 'track'
        else ' ({} tracks)'.format(music[queue_type]['total_tracks'])
    )

    # handle confirmation & request
    if not yes:
        click.confirm(
            'Add {} "{}"{} to the queue?'.format(queue_type, name, total_tracks_str),
            abort=True
        )

    endpoint = 'me/player/queue?uri=' + uri
    Spotify.request(
        endpoint, method='POST',
        handle_errs={}
    )
    if not quiet:
        click.echo('"{}" added to the queue.'.format(name))

    return
