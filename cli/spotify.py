import click

from cli.utils.classes import AliasedGroup

from cli.commands.auth import auth
from cli.commands.status import status
from cli.commands.play import play
from cli.commands.pause import pause
from cli.commands.next import _next
from cli.commands.previous import previous
from cli.commands.devices import devices
from cli.commands.volume import volume


# CLI group
@click.command(
    cls=AliasedGroup,
    options_metavar='[<options>]',
    subcommand_metavar='<command>'
)
@click.version_option(message='spotify-cli, version %(version)s')
def cli():
    pass

# commands
cli.add_command(auth)
cli.add_command(status)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(_next)
cli.add_command(previous)
cli.add_command(devices)
cli.add_command(volume)
