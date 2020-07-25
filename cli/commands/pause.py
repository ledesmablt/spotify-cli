import click

from cli.utils import Spotify


@click.command(options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
def pause(verbose=0, quiet=False):
    """Pause playback."""
    Spotify.request('me/player/pause', method='PUT', ignore_errs=[403])

    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose, _override={'is_playing': False})


    return
