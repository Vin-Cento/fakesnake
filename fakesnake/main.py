#!/usr/bin/env python

import click

from .creation import *


@click.group()
def cli():
    pass


@click.command()
@click.argument("num", type=int)
@click.option("--dist", type=float, default=1)
def shape(num, dist):
    create_shapes(num, dist)


@click.command()
@click.argument("num", type=int)
def name(num):
    create_names(num)


@click.command()
@click.argument("num", type=int)
def email(num):
    create_emails(num)


@click.command()
@click.argument("num", type=int)
def address(num):
    create_addresses(num)


@click.command()
@click.argument("num", type=int)
def password(num):
    create_passwords(num)


@click.command()
@click.argument("num", type=int)
def number(num):
    create_numbers(num)


cli.add_command(shape)
cli.add_command(name)
cli.add_command(email)
cli.add_command(address)
cli.add_command(password)
cli.add_command(number)


def main():
    cli()


if __name__ == "__main__":
    main()
