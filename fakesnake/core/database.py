import psycopg2
import pandas as pd
from sqlalchemy import create_engine, URL

from core import create_texts, create_uuid, create_shapes#, get_table_value

from rich.console import Console
from rich.table import Table
from utils import get_table_description, get_table_relationship
from collections import defaultdict
from utils import DB
from os import listdir


def get_db_config():
    """Show the database config"""
    for key in DB:
        print(DB[key])


def init():
    if ".env" in listdir():
        print(".env exist")
    else:
        with open(".env", "w") as file:
            file.writelines(
                [
                    "DB_PORT=\n",
                    "DB_NAME=\n",
                    "DB_HOST=\n",
                    "DB_PASS=\n",
                    "DB_USER=\n",
                    "DB_TYPE=\n",
                ]
            )
        print(".env created")

def show_table(table: str):
    with psycopg2.connect(
        host=DB["host"],
        database=DB["name"],
        user=DB["user"],
        password=DB["pass"],
        port=DB["port"],
    ) as conn:
        # Create a cursor object to execute SQL queries
        try:
            with conn.cursor() as cursor:
                if table is None:
                    # show all tables
                    cursor.execute(
                        "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
                    )
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                else:
                    cursor.execute(f"SELECT * FROM {table};")
                    results = cursor.fetchall()
                    for row in results:
                        print(row)

        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def show_tables():
    with psycopg2.connect(
        host=DB["host"],
        database=DB["name"],
        user=DB["user"],
        password=DB["pass"],
        port=DB["port"],
    ) as conn:
        # Create a cursor object to execute SQL queries
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
                )
                results = cursor.fetchall()
                for row in results:
                    print(row)
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def inserts(filepath: str, table: str, quotechar: str):
    pg_url = URL.create(
        "postgresql+psycopg2",
        username=DB["user"],
        password=DB["pass"],
        host=DB["host"],
        port=DB["port"],
        database=DB["name"],
    )
    engine = create_engine(pg_url)

    for df in pd.read_csv(
        filepath,
        delimiter=",",
        quotechar=quotechar,
        chunksize=100_000,
        encoding="utf-8",
    ):
        # df = pd.read_csv(filepath, delimiter=",", quotechar="'")
        df.to_sql(table, con=engine, if_exists="append", index=False)

    print(f"upload to {table}")


# def insert_table(table: str):
#     description = get_table_description(table)
#     relation = get_table_relationship(table)
#     special_rules = defaultdict(lambda: None)
#     # read in special rules
#     for row in relation:  # type: ignore
#         special_rules[row[1]] = (row[2], row[3])  # type: ignore
#
#     data = dict()
#     # generate data for each column
#     for col_name, dtype, charlimit, default in description:  # type: ignore
#         # print(col_name, dtype, charlimit, default)
#         # print(special_rules[col_name])
#         if default is None:  # type: ignore
#             if special_rules[col_name]:
#                 print(special_rules)
#                 query = f"select {special_rules[col_name][1]} from {special_rules[col_name][0]}"
#                 get_table_value(table, col_name)
#                 print(query)
#                 continue
#             else:
#                 if dtype == "uuid":
#                     data[col_name] = create_uuid(10)
#
#                 if dtype == "varchar":
#                     if charlimit is None:
#                         data[col_name] = create_texts(10, 255)
#                     else:
#                         data[col_name] = create_texts(10, charlimit)
#                 if dtype == "text":
#                     data[col_name] = create_texts(10, 255)
#
#                 if dtype == "text":
#                     data[col_name] = create_shapes(10, 5)
#         else:
#             continue
#     # print(data)


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
