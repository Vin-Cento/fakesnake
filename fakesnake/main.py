import click
from sqlalchemy import create_engine
from .handler import *
from sqlalchemy.orm import sessionmaker
from .utils.database import DB


@click.group()
def cli():
    pass


@cli.group("gen")
def generate():
    """subcommand for generating data"""
    pass


@cli.group("db")
@click.pass_context
def database(ctx):
    """subcommand for database interaction"""
    ctx.obj = {}
    engine = create_engine(
        f"postgresql://{DB['username']}:{DB['password']}@{DB['hostname']}:{DB['port']}/{DB['dbname']}"
    )
    Session = sessionmaker(bind=engine)
    ctx.obj["session"] = Session()


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
database.add_command(insert_table_handler)
database.add_command(show_table_handler)
database.add_command(show_tables_handler)
database.add_command(exec_handler)
database.add_command(init_handler)


def main():
    cli()


if __name__ == "__main__":
    main()
