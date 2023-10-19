import click

from .creation import *


@click.group()
def cli():
    pass


@click.command()
@click.argument("num", type=int)
@click.option("--dist", type=float, default=1)
def shape(num, dist):
    print("\n".join(create_shapes(num, dist)))


@click.command()
@click.argument("num", type=int)
def name(num):
    print("\n".join(create_names(num)))


@click.command()
@click.argument("num", type=int)
def email(num):
    print("\n".join(create_emails(num)))


@click.command()
@click.argument("num", type=int)
def address(num):
    print("\n".join(create_addresses(num)))


@click.command()
@click.argument("num", type=int)
@click.option("--min", type=int, default=15)
@click.option("--max", type=int, default=25)
def password(num, min, max):
    print("\n".join(create_passwords(num, min, max)))


@click.command()
@click.argument("num", type=int)
def number(num):
    print("\n".join(create_numbers(num)))


cli.add_command(shape)
cli.add_command(name)
cli.add_command(email)
cli.add_command(address)
cli.add_command(password)
cli.add_command(number)


def main():
    cli()


if __name__ == "__main__":
    main()
