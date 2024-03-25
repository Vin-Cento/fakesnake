from sqlalchemy import text
from sqlalchemy.orm import Session

from .creation import (
    create_emails,
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
    """Get the description of a table in the database
    Args:
        table (str): table name
        session (Session): sqlalchemy session
    Returns:
        list: list of tuples containing the column name, data type, character limit, and default value
    """
    query = f"SELECT column_name, udt_name, character_maximum_length, column_default FROM information_schema.columns WHERE table_name = '{table}';"
    results = session.execute(text(query)).fetchall()
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
    results = session.execute(text(query)).fetchall()
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


def get_table(table: str, session: Session, limit: int = 10):
    results = session.execute(text(f"SELECT * FROM {table} LIMIT {limit};")).fetchall()
    session.close()
    return results


def list_tables(session: Session):
    results = session.execute(
        text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' and table_type='BASE TABLE';"
        )
    ).fetchall()
    session.close()
    return results


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
                # randomly sample values from the foreign table of size 10
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
                    elif "email" in col_name.lower():
                        data[col_name] = create_emails(num)
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
                    elif "email" in col_name.lower():
                        data[col_name] = create_emails(num)
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
                    elif "email" in col_name.lower():
                        data[col_name] = create_emails(num)
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


def execute_cmd(query: str, session: Session):
    if query.lower().startswith("select"):
        res = session.execute(text(query))
        for r in res:
            print(r)
    else:
        session.execute(text(query))
        session.commit()
    session.close()
