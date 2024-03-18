import psycopg2

from os import getcwd, listdir

from dotenv import dotenv_values


DB = dict()
if ".env" in listdir(getcwd()):
    v = dotenv_values(f"{getcwd()}/.env")

    # Access the variables
    for e in v.keys():
        DB[e] = v[e]
else:
    print("in default")
    DB["port"] = "5432"
    DB["name"] = "postgres"
    DB["host"] = "localhost"
    DB["pass"] = ""
    DB["user"] = "postgres"


def get_table_description(table):
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


def get_table_value(table, column):
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


def get_table_relationship(table):
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


def get_shapetype(table: str, col: str):
    with psycopg2.connect(
        host=DB["host"],
        database=DB["name"],
        user=DB["user"],
        password=DB["pass"],
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
                string_col = [f'"{c}"' for c in columns]
                query = f"INSERT INTO {table} ({','.join(string_col)}) VALUES ({','.join(['%s' for _ in columns])});"

                cursor.executemany(query, insert_data)
                conn.commit()
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)


def run_command(query):
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
                # Execute SQL queries using the cursor
                cursor.execute(query)

                # Fetch the results of the query
                if query.lower().startswith("select"):
                    results = cursor.fetchall()

                    # Process the results as needed
                    for row in results:
                        print(row)
                else:
                    conn.commit()
        except psycopg2.errors.QueryCanceled as e:
            print("Query was canceled:", e)
