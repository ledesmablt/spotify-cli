import click

from commands.auth import auth
from commands.status import status


@click.group()
def cli():
    pass

cli.add_command(auth)
cli.add_command(status)


if __name__ == '__main__':
    cli()
