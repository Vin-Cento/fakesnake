from os import listdir, path
import platform

from dotenv import dotenv_values
import click


def utils_getDB():
    DB = dict()
    if platform.system() == "Linux":
        folder = f"{path.expanduser('~')}/.config/fakesnake"
        if ".env" in listdir(folder):
            v = dotenv_values(f"{folder}/.env")

            for e in v.keys():
                DB[e] = v[e]
        else:
            print(
                f"""
            Missing .env
            Run: fakes db init
            """
            )
        return DB
    else:
        print("only available on linux")
        exit()


def print_column(
    col,
    string_limit=24,
    color=["blue", "magenta", "red", "green", "cyan", "yellow", "white"],
):
    columns_total = len(col)
    color_len = len(color)
    for i, r in enumerate(col):
        if i == columns_total - 1:
            if type(r) == str:
                click.echo(click.style(f"{r[:string_limit]}", fg=color[i % color_len]))
            else:
                click.echo(r)
        else:
            if type(r) == str:
                click.echo(
                    click.style(f"{r[:string_limit]},", fg=color[i % color_len]),
                    nl=False,
                )
            else:
                click.echo(click.style(f"{r},", fg=color[i % color_len]), nl=False)


def print_row(
    row,
    string_limit=24,
    color=["blue", "magenta", "red", "green", "cyan", "yellow", "white"],
):
    for r in row:  # type: ignore
        print_column(r, string_limit, color)
