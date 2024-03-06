import click

from core import *


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--dist", "-d", type=float, default=1)
@click.option("--header", "-h", type=str, default=None)
def shape(num, dist, header):
    print("\n".join(create_shapes(num, dist, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--dist", "-d", type=float, default=1)
def geojson(num, dist):
    print(create_geojson(num, dist))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def name(num, header):
    print("\n".join(create_names(num, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def email(num, header):
    print("\n".join(create_emails(num, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def address(num, header):
    print("\n".join(create_addresses(num, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--min", "-l", type=int, default=15)
@click.option("--max", "-u", type=int, default=25)
@click.option("--header", "-h", type=str, default=None)
def password(num, min, max, header):
    print("\n".join(create_passwords(num, min, max, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def number(num, header):
    print("\n".join(create_numbers(num, header)))


@click.command()
@click.option("--num", "-n", type=int, default=10)
@click.option("--max", "-m", type=int, default=100)
@click.option("--header", "-h", type=str, default=None)
def text(num, max, header):
    print("\n".join(create_texts(num, max, header)))


@click.command("table")
@click.argument("name")
def table_show(name: str):
    """Show the database"""
    show_table(name)


@click.command("tables")
def tables_show():
    """Show the database"""
    show_tables()

@click.command("describe")
@click.argument("name")
def table_describe(name: str):
    """Show the database"""
    describe_table(name)

@click.command("shows")
def db_shows():
    """Show the database config"""
    for key in DB:
        print(DB[key])


@click.command()
def config():
    print("show command")
