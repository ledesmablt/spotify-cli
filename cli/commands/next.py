import click

from cli.utils import Spotify


@click.command(name='next')
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', is_flag=True)
def _next(verbose=0, quiet=False):
    Spotify.request('me/player/next', method='POST')
    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose)

    return
