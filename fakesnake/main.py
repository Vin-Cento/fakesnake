import click

from fakesnake.creation import *
import fakesnake.setting as setting


@click.group()
def cli():
    pass


@click.command()
@click.argument("num", type=int)
@click.option("--dist", "-d", type=float, default=1)
@click.option("--header", "-h", type=str, default="Shape")
def shape(num, dist, header):
    print("\n".join(create_shapes(num, dist, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", "-h", type=str, default="Name")
def name(num, header):
    print("\n".join(create_names(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", "-h", type=str, default="Email")
def email(num, header):
    print("\n".join(create_emails(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", "-h", type=str, default="Address")
def address(num, header):
    print("\n".join(create_addresses(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--min", "-l", type=int, default=15)
@click.option("--max", "-u", type=int, default=25)
@click.option("--header", "-h", type=str, default="Password")
def password(num, min, max, header):
    print("\n".join(create_passwords(num, min, max, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--header", "-h", type=str, default="Number")
def number(num, header):
    print("\n".join(create_numbers(num, header)))


@click.command()
@click.argument("num", type=int)
@click.option("--min", type=int, default=100)
@click.option("--header", "-h", type=str, default="Text")
def text(num, header):
    print("\n".join(create_texts(num, header)))


@click.command()
def config():
    setting.list()


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("table", type=str)
@click.option("--user", "-u", type=str, default="")
@click.option("--database_name", "-d", type=str, default="")
@click.option("--host", "-h", type=str, default="")
@click.option("--port", "-p", type=str, default="")
@click.option("--password", "-P", type=str, default="")
def insert(input, table, user, database_name, host, port, password):
    from fakesnake.setting import DB

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

    inserts(input, table, db_setting)


cli.add_command(shape)
cli.add_command(name)
cli.add_command(email)
cli.add_command(address)
cli.add_command(password)
cli.add_command(number)
cli.add_command(config)
cli.add_command(insert)


def main():
    cli()


if __name__ == "__main__":
    main()
