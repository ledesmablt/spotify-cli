import click

from commands.auth import auth
from commands.status import status
from commands.play import play
from commands.pause import pause
from commands.next import _next
from commands.prev import prev
from commands.devices import devices


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


if __name__ == '__main__':
    cli()
