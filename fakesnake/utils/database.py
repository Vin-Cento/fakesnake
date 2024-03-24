from sqlalchemy import text
from sqlalchemy.orm import Session


def get_table_description(table, session: Session):
    query = f"SELECT column_name, udt_name, character_maximum_length, column_default FROM information_schema.columns WHERE table_name = '{table}';"
    return session.execute(text(query))


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
    return results


def get_shapetype(table: str, col: str, session: Session):
    query = f"SELECT type FROM geometry_columns WHERE f_table_name = '{table}' and f_geometry_column = '{col}';"
    result = session.execute(text(query))
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
