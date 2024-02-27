import click

from core import *
from setting import *


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


@click.command()
def config():
    list()


@click.command()
def init():
    init()


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("table", type=str)
@click.option("--quotechar", "-D", type=str, default='"')
@click.option("--user", "-u", type=str, default="")
@click.option("--database_name", "-d", type=str, default="mydb")
@click.option("--host", "-h", type=str, default="")
@click.option("--port", "-p", type=str, default="")
@click.option("--password", "-P", type=str, default="")
def insert(input, table, quotechar, user, database_name, host, port, password):
    from setting import DB

    db_setting = {
        "port": DB["port"],
        "name": DB["name"],
        "host": DB["host"],
        "pass": DB["pass"],
        "user": DB["user"],
    }

    custom_setting = {
        "user": user,
        "name": database_name,
        "host": host,
        "port": port,
        "pass": password,
    }
    for k in custom_setting:
        if custom_setting[k] != "":
            db_setting[k] = custom_setting[k]

    inserts(input, table, quotechar, db_setting)
