import click
from core import *
from handler import *


@click.group()
def cli():
    pass


cli.add_command(shape)
cli.add_command(geojson)
cli.add_command(name)
cli.add_command(email)
cli.add_command(address)
cli.add_command(password)
cli.add_command(number)
cli.add_command(config)
cli.add_command(insert)
cli.add_command(init)
cli.add_command(text)


def main():
    cli()


if __name__ == "__main__":
    main()
