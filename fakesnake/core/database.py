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
from os import listdir, path
import click
import platform


def get_table_description(table, session: Session):
    query = f"SELECT column_name, udt_name, character_maximum_length, column_default FROM information_schema.columns WHERE table_name = '{table}';"
    results = session.execute(text(query))
    session.close()
    return results


def get_table_value(table, column, session: Session):
    query = f'SELECT {column} FROM "{table}";'
    results = session.execute(text(query))
    session.close()
    return results


def get_table_relationship(table, session: Session):
    query = f"""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
            WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name ='{table}'
            GROUP BY tc.table_name, kcu.column_name, foreign_table_name, foreign_column_name;
        """
    results = session.execute(text(query))
    session.close()
    return results


def get_shapetype(table: str, col: str, session: Session):
    query = f"SELECT type FROM geometry_columns WHERE f_table_name = '{table}' and f_geometry_column = '{col}';"
    result = session.execute(text(query))
    session.close()
    return result[0]  # type: ignore


def insert_sql(table: str, data, session: Session):
    insert_data = []
    columns = list(data.keys())
    for i in range(len(data[columns[0]])):  # type: ignore
        row = {}
        for key in data.keys():
            row[key] = data[key][i]
        insert_data.append(row)

    string_col = [f'"{c}"' for c in columns]
    query = f"INSERT INTO {table} ({','.join(string_col)}) VALUES ({','.join([f':{col}' for col in columns])});"
    print(query)

    session.execute(text(query), insert_data)
    session.commit()
    session.close()


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


def show_table(table: str, session: Session):
    t = Table(title=f"Table: {table}")
    description = get_table_description(table, session)
    for i in description:  # type: ignore
        t.add_column(i[0], justify="right", style="cyan")

    results = session.execute(text(f"SELECT * FROM {table} LIMIT 10;"))
    session.close()
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


def show_tables(session: Session):
    results = session.execute(
        text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' and table_type='BASE TABLE';"
        )
    )
    session.close()
    for row in results:
        print(row[0])


def insert_table(table: str, num: int, session: Session) -> None:
    description = get_table_description(table, session)
    relation = get_table_relationship(table, session)
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
                res = get_table_value(special_rules[col_name][0], special_rules[col_name][1].replace(",", ""), session)  # type: ignore
                # randonmly sample values from the foreign table of size 10
                if res == None:
                    raise ValueError(
                        f"Foreign table {special_rules[col_name][0]} not found"  # type: ignore
                    )

                if len(res) == 0:  # type: ignore
                    raise ValueError(
                        f"Foreign table {special_rules[col_name][0]} is empty"  # type: ignore
                    )
                data[col_name] = [res[i % len(res)][0] for i in range(num)]  # type: ignore
            else:
                if dtype == "uuid":
                    data[col_name] = create_uuid(num)

                if dtype == "geometry":
                    shp_type = get_shapetype(table, col_name, session)
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

    insert_sql(table, data, session)


def describe_table(table: str, session: Session):
    t = Table(title=f"Table: {table}")
    t.add_column("column", justify="right", style="cyan", no_wrap=True)
    t.add_column("datatype", style="magenta")
    t.add_column("char_limit", style="magenta")
    t.add_column("default", justify="right", style="green")

    print("description of table", table)
    results = get_table_description(table, session)
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
    results = get_table_relationship(table, session)

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
