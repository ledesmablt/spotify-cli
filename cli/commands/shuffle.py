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
@click.argument(
    'mode', type=click.Choice(['on', 'off'], case_sensitive=False)
)
def shuffle(mode, verbose=0, quiet=False, wait=True):
    """Turn shuffle on or off."""
    requests = [{
        'endpoint': 'me/player/shuffle?state={}'.format('true' if mode == 'on' else 'false'),
        'method': 'PUT'
    }]
    Spotify.multirequest(requests, wait=wait)
    if quiet:
        return

    if verbose == 0:
        click.echo('Shuffle turned {}.'.format(mode))
    else:
        from cli.commands.status import status
        status.callback(verbose=verbose, override={'is_shuffle': mode == 'on'})

    return
