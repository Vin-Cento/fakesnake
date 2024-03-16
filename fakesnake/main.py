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


generate.add_command(shape_handler)
generate.add_command(geojson_handler)
generate.add_command(name_handler)
generate.add_command(email_handler)
generate.add_command(address_handler)
generate.add_command(password_handler)
generate.add_command(number_handler)
generate.add_command(text_handler)

database.add_command(db_shows)
database.add_command(describe_table_handler)
database.add_command(table_insert)

database.add_command(exec_handler)


show_db.add_command(show_table_handler)
show_db.add_command(show_tables_handler)


def main():
    cli()


if __name__ == "__main__":
    main()
