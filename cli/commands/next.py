import click

from cli.utils import Spotify


@click.command(name='next', options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '-q', '--quiet', is_flag=True,
    help='Suppress output.'
)
def _next(verbose=0, quiet=False):
    """Play the next song in the queue."""
    Spotify.request('me/player/next', method='POST')
    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose)

    return
