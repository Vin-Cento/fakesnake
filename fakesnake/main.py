import click
from core import *
from handler import *


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

show_db.add_command(table_show)
# database.add_command(config)
# database.add_command(insert)
# database.add_command(show)
# database.add_command(init)

if __name__ == "__main__":
    cli()
