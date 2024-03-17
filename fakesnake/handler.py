import click

from .core.creation import *
from .core.database import *


@click.command("shape")
@click.option("--num", "-n", type=int, default=10)
@click.option("--dist", "-d", type=float, default=1)
@click.option("--header", "-h", type=str, default=None)
def shape_handler(num, dist, header):
    """generate a list of shape"""
    print("\n".join(create_shapes(num, dist, header)))


@click.command("geojson")
@click.option("--num", "-n", type=int, default=10)
@click.option("--dist", "-d", type=float, default=1)
def geojson_handler(num, dist):
    """generate a list of geojson"""
    print(create_geojson(num, dist))


@click.command("name")
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def name_handler(num, header):
    """generate a list of name"""
    print("\n".join(create_names(num, header)))


@click.command("email")
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def email_handler(num, header):
    """generate a list of email"""
    print("\n".join(create_emails(num, header)))


@click.command("address")
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def address_handler(num, header):
    """generate a list of address"""
    print("\n".join(create_addresses(num, header)))


@click.command("password")
@click.option("--num", "-n", type=int, default=10)
@click.option("--min", "-l", type=int, default=15)
@click.option("--max", "-u", type=int, default=25)
@click.option("--header", "-h", type=str, default=None)
def password_handler(num, min, max, header):
    """generate a list of password"""
    print("\n".join(create_passwords(num, min, max, header)))


@click.command("number")
@click.option("--num", "-n", type=int, default=10)
@click.option("--header", "-h", type=str, default=None)
def number_handler(num, header):
    """generate a list of number"""
    numbers = [str(n) for n in create_numbers(num, header)]
    print("\n".join(numbers))


@click.command("text")
@click.option("--num", "-n", type=int, default=10)
@click.option("--max", "-m", type=int, default=100)
@click.option("--header", "-h", type=str, default=None)
def text_handler(num, max, header):
    """generate a list of text"""
    print("\n".join(create_texts(num, max, header)))


@click.command("table")
@click.argument("table")
def show_table_handler(table: str):
    """show all columns the table"""
    show_table(table)


@click.command("tables")
def show_tables_handler():
    """show all tables the database"""
    show_tables()


@click.command("describe")
@click.argument("table")
def describe_table_handler(table: str):
    """describe the current database"""
    describe_table(table)


@click.command("insert")
@click.argument("table")
@click.option("--num", "-n", type=int, default=10)
def table_insert(table: str, num: int):
    """insert random data into table"""
    insert_table(table, num)


@click.command("config")
def config_handler():
    """show the database config"""
    for key in DB:
        print(f"{key}:", DB[key])


@click.command("exec")
@click.argument("query", type=str)
def exec_handler(query: str):
    """execute a sql command"""
    if query == None:
        print("empty")
    else:
        execute_cmd(query)
