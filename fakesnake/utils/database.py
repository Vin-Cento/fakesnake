import psycopg2

from os import listdir, path
import platform

from dotenv import dotenv_values
from sqlalchemy import text
from sqlalchemy.orm import Session


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
else:
    print("only available on linux")
    exit()


def get_table_description(table, session: Session):
    query = f"SELECT column_name, udt_name, character_maximum_length, column_default FROM information_schema.columns WHERE table_name = '{table}';"
    return session.execute(text(query))


def get_table_value(table, column):
    with psycopg2.connect(
        host=DB["hostname"],
        database=DB["dbname"],
        user=DB["username"],
        password=DB["password"],
        port=DB["port"],
    ) as conn:
        try:
            with conn.cursor() as cursor:
                query = f'SELECT {column} FROM "{table}";'
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def get_table_relationship(table):
    with psycopg2.connect(
        host=DB["hostname"],
        database=DB["dbname"],
        user=DB["username"],
        password=DB["password"],
        port=DB["port"],
    ) as conn:
        try:
            with conn.cursor() as cursor:
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
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def get_shapetype(table: str, col: str):
    with psycopg2.connect(
        host=DB["hostname"],
        database=DB["dbname"],
        user=DB["username"],
        password=DB["password"],
        port=DB["port"],
    ) as conn:
        try:
            with conn.cursor() as cursor:
                query = f"SELECT type FROM geometry_columns WHERE f_table_name = '{table}' and f_geometry_column = '{col}';"
                cursor.execute(query)
                result = cursor.fetchall()
                return result[0]

        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


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
