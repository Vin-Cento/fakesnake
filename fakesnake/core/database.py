import psycopg2
from sqlalchemy import text
from sqlalchemy.orm import Session

from .creation import (
    create_texts,
    create_uuid,
    create_shapes,
    create_names,
    create_points,
    create_ints,
    create_numbers,
)

from rich.console import Console
from rich.table import Table
from collections import defaultdict
from ..utils.database import (
    DB,
    get_table_description,
    get_table_relationship,
    get_table_value,
    insert_sql,
    get_shapetype,
    run_command,
)
from os import listdir, path
import click
import platform


def init_db():
    if platform.system() == "Linux":
        folder = f"{path.expanduser('~')}/.config/fakesnake"
        if ".env" in listdir(folder):
            print(".env exist")
        else:
            hostname = click.prompt("Enter hostname", type=str)
            username = click.prompt("Enter username", type=str)
            password = click.prompt("Enter password", type=str)
            port = click.prompt("Enter port", type=int)
            dbname = click.prompt("Enter dbname", type=str)
            dbtype = click.prompt("Enter dbtype", type=click.Choice(["postgres"]))
            with open(f"{folder}/.env", "w") as file:
                file.writelines(
                    [
                        f"username={username}\n",
                        f"hostname={hostname}\n",
                        f"dbname={dbname}\n",
                        f"password={password}\n",
                        f"port={port}\n",
                        f"dbtype={dbtype}\n",
                    ]
                )
            print(".env created")
    else:
        print("this only works on Linux at the moment")


def show_table(table: str):
    with psycopg2.connect(
        host=DB["hostname"],
        database=DB["dbname"],
        user=DB["username"],
        password=DB["password"],
        port=DB["port"],
    ) as conn:
        # Create a cursor object to execute SQL queries
        try:
            with conn.cursor() as cursor:
                t = Table(title=f"Table: {table}")
                description = get_table_description(table)
                for i in description:  # type: ignore
                    t.add_column(i[0], justify="right", style="cyan")

                cursor.execute(f"SELECT * FROM {table} LIMIT 10;")
                results = cursor.fetchall()
                for row in results:
                    try:
                        t.add_row(*row)  # type: ignore
                    except:
                        new_row = ()
                        for r in row:
                            new_row += (str(r),)
                        t.add_row(*new_row)
                console = Console()
                console.print(t)

        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def show_tables():
    with psycopg2.connect(
        host=DB["hostname"],
        database=DB["dbname"],
        user=DB["username"],
        password=DB["password"],
        port=DB["port"],
    ) as conn:
        # Create a cursor object to execute SQL queries
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public' and table_type='BASE TABLE';"
                )
                results = cursor.fetchall()
                for row in results:
                    print(row[0])
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def insert_table(table: str, num: int) -> None:
    description = get_table_description(table)
    relation = get_table_relationship(table)
    special_rules = defaultdict(lambda: None)
    # read in special rules
    for _, mainCol, foreignTable, foreignCol in relation:  # type: ignore
        special_rules[mainCol] = (foreignTable, foreignCol)  # type: ignore

    data = dict()

    col_names = []
    for col_name, dtype, charlimit, default in description:  # type: ignore
        col_names.append(col_name)
        if default is None:  # type: ignore
            if special_rules[col_name]:
                res = get_table_value(special_rules[col_name][0], special_rules[col_name][1].replace(",", ""))  # type: ignore
                # randonmly sample values from the foreign table of size 10
                if res == None:
                    raise ValueError(
                        f"Foreign table {special_rules[col_name][0]} not found"  # type: ignore
                    )

                if len(res) == 0:
                    raise ValueError(
                        f"Foreign table {special_rules[col_name][0]} is empty"  # type: ignore
                    )
                data[col_name] = [res[i % len(res)][0] for i in range(num)]
            else:
                if dtype == "uuid":
                    data[col_name] = create_uuid(num)

                if dtype == "geometry":
                    shp_type = get_shapetype(table, col_name)
                    if shp_type[0] == "POINT":  # type: ignore
                        data[col_name] = create_points(num)
                    else:
                        data[col_name] = create_shapes(num, 4)

                if dtype == "varchar":
                    if "name" in col_name.lower():
                        if charlimit is None:
                            data[col_name] = create_names(num)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_names(num, max_nb_chars=charlimit)
                    else:
                        if charlimit is None:
                            data[col_name] = create_texts(num, 255)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_texts(num, charlimit)

                if dtype == "bpchar":
                    if "name" in col_name.lower():
                        if charlimit is None:
                            data[col_name] = create_names(num)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_names(num, max_nb_chars=charlimit)
                    else:
                        if charlimit is None:
                            data[col_name] = create_texts(num, 255)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_texts(num, charlimit)

                if dtype == "text":
                    if "name" in col_name:
                        if charlimit is None:
                            data[col_name] = create_names(num)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_names(num, max_nb_chars=charlimit)
                    else:
                        if charlimit is None:
                            data[col_name] = create_texts(num, 255)
                        elif charlimit < 6:
                            data[col_name] = create_names(num, charlimit)
                        else:
                            data[col_name] = create_names(num, charlimit)

                if "float" in dtype:
                    data[col_name] = create_numbers(num)

                if "int" in dtype:
                    data[col_name] = create_ints(num)
        else:
            continue

    insert_sql(table, data)


def describe_table(table: str):
    t = Table(title=f"Table: {table}")
    t.add_column("column", justify="right", style="cyan", no_wrap=True)
    t.add_column("datatype", style="magenta")
    t.add_column("char_limit", style="magenta")
    t.add_column("default", justify="right", style="green")

    results = get_table_description(table)
    if results is None:
        print("Table not found")
        return
    for row in results:
        t.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]))  # type: ignore

    console = Console()
    console.print(t)

    t = Table(title=f"Relationship")
    t.add_column("table", justify="right", style="cyan", no_wrap=True)
    t.add_column("column", style="green")
    t.add_column("foreign_table", justify="right", style="cyan", no_wrap=True)
    t.add_column("foreign_column", justify="right", style="green")
    results = get_table_relationship(table)

    if results is None:
        print("Table not found")
    else:
        for row in results:
            t.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]))  # type: ignore
        console = Console()
        console.print(t)


def execute_cmd(query: str, session: Session):
    if query.lower().startswith("select"):
        res = session.execute(text(query))
        for r in res:
            print(r)
    else:
        session.execute(text(query))
        session.commit()
    session.close()
