"""spotify.py

CLI entry point.
"""

import click

from cli.commands.auth import auth
from cli.commands.browse import browse
from cli.commands.devices import devices
from cli.commands.history import history
from cli.commands.next import _next
from cli.commands.pause import pause
from cli.commands.play import play
from cli.commands.previous import previous
from cli.commands.queue import queue
from cli.commands.repeat import repeat
from cli.commands.save import save
from cli.commands.search import search
from cli.commands.seek import seek
from cli.commands.shuffle import shuffle
from cli.commands.status import status
from cli.commands.toggle import toggle
from cli.commands.top import top
from cli.commands.volume import volume
from cli.utils.classes import AliasedGroup


# CLI group
@click.command(
    cls=AliasedGroup,
    options_metavar='[<options>]',
    subcommand_metavar='<command>'
)
# UPDATED: Add package name to stop click RuntimeError caused by not
# detecting the package_name
@click.version_option(message='spotify-cli, version %(version)s',
                      package_name='spotify-cli')
def cli():
    pass


# Commands
cli.add_command(auth)  # type: ignore
cli.add_command(status)  # type: ignore
cli.add_command(play)  # type: ignore
cli.add_command(pause)  # type: ignore
cli.add_command(_next)  # type: ignore
cli.add_command(previous)  # type: ignore
cli.add_command(devices)  # type: ignore
cli.add_command(volume)  # type: ignore
cli.add_command(shuffle)  # type: ignore
cli.add_command(repeat)  # type: ignore
cli.add_command(save)  # type: ignore
cli.add_command(queue)  # type: ignore
cli.add_command(browse)  # type: ignore
cli.add_command(history)  # type: ignore
cli.add_command(toggle)  # type: ignore
cli.add_command(top)  # type: ignore
cli.add_command(search)  # type: ignore
cli.add_command(seek)  # type: ignore


# For debugging purposes: python -m cli.spotify
if __name__ == "__main__":
    cli()
