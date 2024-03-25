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


# TODO: add option to show whole row or limit to 10
@click.command("table")
@click.argument("table")
@click.pass_context
def show_table_handler(ctx, table: str):
    """show all columns the table"""
    # get columns
    description = get_table_description(table, ctx.obj["session"])
    columns_total = len(description)
    for i, r in enumerate(description):  # type: ignore
        # i[0] is column
        if i == columns_total - 1:
            click.echo(r[0])
        else:
            click.echo(f"{r[0]},", nl=False)

    results = get_table(table, ctx.obj["session"])

    for row in results:
        for i, r in enumerate(row):
            # TODO: add option to show whole row or limit to 10
            if i == columns_total - 1:
                if type(r) == str:
                    click.echo(f"{r[:10]}")
                else:
                    click.echo(f"{r}")  # type: ignore
            else:
                if type(r) == str:
                    click.echo(f"{r[:10]},", nl=False)
                else:
                    click.echo(f"{r},", nl=False)  # type: ignore


@click.command("tables")
@click.pass_context
def show_tables_handler(ctx):
    """show all tables the database"""
    results = list_tables(ctx.obj["session"])

    click.echo(click.style(f"Tables: Total {len(results)}", fg="green"))
    for row in results:
        click.echo(click.style(f"{row[0]}"))


@click.command("describe")
@click.argument("table")
@click.pass_context
def describe_table_handler(ctx, table: str):
    """describe the current database"""
    results = get_table_description(table, ctx.obj["session"])
    if results == []:
        click.echo(click.style("Table not found", fg="red"))
    else:
        click.echo(click.style(f"Table: {table}\n", fg="green"))
        click.echo(click.style(f"column,", fg="blue"), nl=False)
        click.echo(click.style(f"datatype,", fg="magenta"), nl=False)
        click.echo(click.style(f"char_limit,", fg="red"), nl=False)
        click.echo(click.style(f"default", fg="green"))

        for row in results:
            click.echo(click.style(f"{row[0]},", fg="blue"), nl=False)
            click.echo(click.style(f"{row[1]},", fg="magenta"), nl=False)
            click.echo(click.style(f"{row[2]},", fg="red"), nl=False)
            click.echo(click.style(f"{row[3]}", fg="green"))

        results = get_table_relationship(table, ctx.obj["session"])
        if results == []:
            click.echo(click.style("\nNo Relationship found", fg="magenta"))
        else:
            click.echo(click.style(f"\nTable: {table}", fg="green"))
            click.echo(click.style(f"column,", fg="blue"), nl=False)
            click.echo(click.style(f"datatype,", fg="magenta"), nl=False)
            click.echo(click.style(f"char_limit,", fg="red"), nl=False)
            click.echo(click.style(f"default", fg="green"))
            for row in results:
                click.echo(click.style(f"{row[0]},", fg="blue"), nl=False)
                click.echo(click.style(f"{row[1]},", fg="magenta"), nl=False)
                click.echo(click.style(f"{row[2]},", fg="red"), nl=False)
                click.echo(click.style(f"{row[3]}", fg="green"))


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
