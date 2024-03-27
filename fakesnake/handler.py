import click

from fakesnake.utils.utils import print_column, print_row

from .core.creation import *
from .core.database import *


@click.command("shape")
@click.option("--num", "-n", type=int, default=10)
@click.option("--dist", "-d", type=float, default=1)
@click.option("--header", "-h", type=str, default=None)
@click.option("--srid", "-s", type=int, default=4326)
def shape_handler(num, dist, header, srid):
    """generate a list of shape"""
    print("\n".join(create_shapes(num, dist, header, srid)))


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
@click.option("string_limit", "--string_limit", "-s", type=int, default=24)
@click.pass_context
def show_table_handler(ctx, table: str, string_limit: int):
    """show all columns the table"""
    description = get_table_description(table, ctx.obj["session"])
    print_column([d[0] for d in description])

    results = get_table(table, ctx.obj["session"])

    if results == []:
        click.echo("EMPTY")
    else:
        print_row(results, string_limit)


@click.command("tables")
@click.pass_context
def show_tables_handler(ctx):
    """show all tables the database"""
    results = list_tables(ctx.obj["session"])

    click.echo(click.style(f"Tables: Total {len(results)}", fg="green"))
    print_row(results)


@click.command("describe")
@click.argument("table")
@click.pass_context
def describe_table_handler(ctx, table: str):
    """describe the current database"""
    color_theme = ["blue", "magenta", "red", "green"]
    results = get_table_description(table, ctx.obj["session"])
    if results == []:
        click.echo(click.style("Table not found", fg="red"))
    else:
        click.echo(click.style(f"Table: {table}\n", fg="green"))
        print_column(["column", "datatype", "char_limit", "default"], 100, color_theme)
        print_row(results, 100, color_theme)

        results = get_table_relationship(table, ctx.obj["session"])
        if results == []:
            click.echo(click.style("\nNo Relationship found", fg="magenta"))
        else:
            for res in results:
                click.echo(click.style(f"\nRelationship Table: {res[2]}\n", fg="green"))
                print_column(
                    ["column", "datatype", "char_limit", "default"], 100, color_theme
                )
                print_column(res, 100, color_theme)


@click.command("insert")
@click.argument("table")
@click.option("--num", "-n", type=int, default=10)
@click.pass_context
def insert_table_handler(ctx, table: str, num: int):
    """insert random data into table"""
    insert_table(table, num, ctx.obj["session"])


@click.command("config")
@click.pass_context
def config_handler(ctx):
    """show the database config"""
    DB = ctx.obj["DB"]
    for key in DB:
        print(f"{key}:", DB[key])


@click.command("exec")
@click.argument("query", type=str)
@click.pass_context
def exec_handler(ctx, query: str):
    """execute a sql command"""
    print(query)
    if query == None:
        print("empty")
    else:
        execute_cmd(query, ctx.obj["session"])


@click.command("init")
def init_handler():
    init_db()
