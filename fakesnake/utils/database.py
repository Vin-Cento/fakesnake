import psycopg2
from typing import Tuple, Any, List
from os import getcwd, listdir, environ

from dotenv import load_dotenv


DB = dict()
if ".env" in listdir(getcwd()):
    load_dotenv(f"{getcwd()}/.env")

    # Access the variables
    DB["port"] = environ.get("DB_PORT")
    DB["name"] = environ.get("DB_NAME")
    DB["host"] = environ.get("DB_HOST")
    DB["pass"] = environ.get("DB_PASS")
    DB["user"] = environ.get("DB_USER")
else:
    DB["port"] = "5432"
    DB["name"] = "postgres"
    DB["host"] = "localhost"
    DB["pass"] = ""
    DB["user"] = "postgres"


def get_table_description(table) -> List[Tuple[Any]] | None:
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
                # TODO: combine udt_name and character_maximum_length together
                query = f"SELECT column_name, udt_name, character_maximum_length, column_default FROM information_schema.columns WHERE table_name = '{table}';"
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def get_table_value(table, column) -> List[Tuple[Any]] | None:
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
                query = f'SELECT {column} FROM "{table}";'
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def get_table_relationship(table) -> List[Tuple[str]] | None:
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


def insert_sql(table: str, data):
    insert_data = []
    columns = list(data.keys())
    for i in range(len(data[columns[0]])):  # type: ignore
        row = ()
        for key in data.keys():
            row += (data[key][i],)
        insert_data.append(row)

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
                query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s' for _ in columns])});"

                print(query)
                print(insert_data)
                cursor.executemany(query, insert_data)
                conn.commit()
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)
