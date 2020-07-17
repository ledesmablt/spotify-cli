import click

from cli.utils import Spotify


@click.command()
@click.option('-v', '--verbose', count=True)
def pause(verbose=0):
    Spotify.request('me/player/pause', method='PUT')
    if verbose:
        from cli.commands.status import status
        status.callback(verbose=verbose-1)

    return
