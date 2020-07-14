import click

from commands.auth import auth
from commands.status import status
from commands.play import play
from commands.pause import pause
from commands.next import next
from commands.prev import prev


@click.group()
def cli():
    pass

cli.add_command(auth)
cli.add_command(status)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(next)
cli.add_command(prev)


if __name__ == '__main__':
    cli()
