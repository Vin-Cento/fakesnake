import click

# from .core.creation import *
# from .core.database import *

from .handler import *


@click.group()
def cli():
    pass


@cli.group("gen")
def generate():
    pass


@cli.group("db")
def database():
    pass


@database.group("show")
def show_db():
    pass


generate.add_command(shape)
generate.add_command(geojson)
generate.add_command(name)
generate.add_command(email)
generate.add_command(address)
generate.add_command(password)
generate.add_command(number)
generate.add_command(text)

database.add_command(db_shows)
database.add_command(table_describe)
database.add_command(table_insert)


show_db.add_command(table_show)
show_db.add_command(tables_show)


def main():
    cli()


if __name__ == "__main__":
    main()
