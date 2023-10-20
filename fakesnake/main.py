import click

from .creation import *


@click.group()
def cli():
    pass


@click.command()
@click.argument("num", type=int)
@click.option("--dist", type=float, default=1)
@click.option("--header", type=str, default="Shape")
def shape(num, dist, header):
    print("\n".join(create_shapes(num, dist, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", type=str, default="Name")
def name(num, header):
    print("\n".join(create_names(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", type=str, default="Email")
def email(num, header):
    print("\n".join(create_emails(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", type=str, default="Address")
def address(num, header):
    print("\n".join(create_addresses(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--min", type=int, default=15)
@click.option("--max", type=int, default=25)
@click.option("--header", type=str, default="Password")
def password(num, min, max, header):
    print("\n".join(create_passwords(num, min, max, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", type=str, default="Number")
def number(num, header):
    print("\n".join(create_numbers(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--min", type=int, default=100)
@click.option("--header", type=str, default="Text")
def text(num, header):
    print("\n".join(create_texts(num, header)))


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("table", type=str)
def insert(input, table):
    inserts(input, table)


cli.add_command(shape)
cli.add_command(name)
cli.add_command(email)
cli.add_command(address)
cli.add_command(password)
cli.add_command(number)
cli.add_command(insert)


def main():
    cli()


if __name__ == "__main__":
    main()
