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
def play(verbose=0, quiet=False, shuffle=None, repeat=None):
    """Resume playback."""
    requests = []
    if shuffle:
        from cli.commands.shuffle import shuffle as shuffle_cmd
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
    Spotify.request('me/player/play', method='PUT', ignore_errs=[403])

    if not quiet:
        from cli.commands.status import status
        status.callback(verbose=verbose, _override={'is_playing': True})

    return
