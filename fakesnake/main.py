import click
from .handler import *


@click.group()
def cli():
    pass


@cli.group("gen")
def generate():
    """subcommand for generating data"""
    pass


@cli.group("db")
def database():
    """subcommand for database interaction"""
    pass


generate.add_command(shape_handler)
generate.add_command(geojson_handler)
generate.add_command(name_handler)
generate.add_command(email_handler)
generate.add_command(address_handler)
generate.add_command(password_handler)
generate.add_command(number_handler)
generate.add_command(text_handler)
database.add_command(config_handler)
database.add_command(describe_table_handler)
database.add_command(table_insert)
database.add_command(show_table_handler)
database.add_command(show_tables_handler)
database.add_command(exec_handler)


def main():
    cli()


if __name__ == "__main__":
    main()
