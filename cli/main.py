import click

from cli.commands.auth import auth
from cli.commands.status import status
from cli.commands.play import play
from cli.commands.pause import pause
from cli.commands.next import _next
from cli.commands.prev import prev
from cli.commands.devices import devices
from cli.commands.volume import volume


@click.group()
def cli():
    pass

cli.add_command(auth)
cli.add_command(status)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(_next)
cli.add_command(prev)
cli.add_command(devices)
cli.add_command(volume)
