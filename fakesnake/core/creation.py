from faker import Faker
from faker.providers import geo

from numpy import random
from tqdm import tqdm

from random import randint
from typing import List

from utils import create_square


def create_shapes(num, dist, header=None) -> List[str]:
    fake = Faker()
    fake.add_provider(geo)
    polygons = [header] if header else []
    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        polygons.append(square_polygon.__str__().replace("\n", ""))
    return polygons


def create_names(num, header=None) -> List[str]:
    fake = Faker()
    names = [header] if header else []
    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        names.append(f"'{fake.name()}'")
    return names


def create_emails(num, header=None) -> List[str]:
    fake = Faker()
    emails = [header] if header else []
    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        emails.append(f"'{fake.email()}'")
    return emails


def create_addresses(num, header=None) -> List[str]:
    fake = Faker()
    addresses = [header] if header else []
    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        street_address = fake.street_address()
        # Generate a random city
        city = fake.city()
        # Generate a random state
        state = fake.state()
        # Generate a random postal code
        postal_code = fake.postcode()
        # Combine the parts to create an address
        addresses.append(f"'{street_address}, {city}, {state}, {postal_code}'")
    return addresses


def create_passwords(num, min, max, header=None) -> List[str]:
    assert min > 3, "min should be greater than 3"
    assert (
        max >= min
    ), "max should be greater than or equal to min, (default for max is 25)"

    fake = Faker()
    passwords = [header] if header else []

    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        passwords.append(f"'{fake.password(length=randint(min, max),)}'")
    return passwords


def create_numbers(num, header=None) -> List[str]:
    nums = [header] if header else []
    d_bool = False if num > 5000 else True
    for i in tqdm(random.normal(0, 1, num), disable=d_bool):
        nums.append(i)
    return nums


def create_texts(num, max, header=None) -> List[str]:
    fake = Faker()
    texts = [header] if header else []
    d_bool = False if num > 5000 else True
    for _ in tqdm(range(num), disable=d_bool):
        texts.append(f"'{fake.text(max_nb_chars=max)}'")
    return texts


def inserts(filepath: str, table: str, quotechar: str, db_setting):
    import pandas as pd

    from sqlalchemy import create_engine, URL

    # pg_url = URL.create(
    #     "postgresql+psycopg2",
    #     username=db_setting["user"],
    #     password=db_setting["pass"],
    #     host=db_setting["host"],
    #     port=db_setting["port"],
    #     database=db_setting["name"],
    # )
    # engine = create_engine(pg_url)
    engine = create_engine(f'sqlite:///{db_setting["name"]}.db', echo=False)

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
