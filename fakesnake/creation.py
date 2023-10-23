from geopy import Point
from geopy.distance import distance
from shapely.geometry import Polygon

from faker import Faker
from faker.providers import geo

from numpy import random
from tqdm import tqdm

from random import randint


def create_square(lat, lon, edge_length):
    center = Point(lat, lon)
    north = distance(miles=edge_length).destination(center, 45)
    east = distance(miles=edge_length).destination(center, 135)
    south = distance(miles=edge_length).destination(center, 225)
    west = distance(miles=edge_length).destination(center, 315)

    square_points = [north, east, south, west]
    polygon = Polygon([(p.longitude, p.latitude) for p in square_points])

    return polygon


def create_shapes(num, dist, header):
    fake = Faker()
    fake.add_provider(geo)
    polygons = [header]
    for _ in tqdm(range(num)):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        polygons.append(square_polygon.__str__().replace("\n", ""))
    return polygons


def create_names(num, header):
    fake = Faker()
    names = [header]
    for _ in tqdm(range(num)):
        names.append(f"'{fake.name()}'")
    return names


def create_emails(num, header):
    fake = Faker()
    emails = [header]
    for _ in tqdm(range(num)):
        emails.append(f"'{fake.email()}'")
    return emails


def create_addresses(num, header):
    fake = Faker()
    addresses = [header]
    for _ in tqdm(range(num)):
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


def create_passwords(num, min, max, header):
    assert min > 3, "min should be greater than 3"
    assert (
        max >= min
    ), "max should be greater than or equal to min, (default for max is 25)"

    fake = Faker()
    passwords = [header]

    for _ in tqdm(range(num)):
        passwords.append(f"'{fake.password(length=randint(min, max),)}'")
    return passwords


def create_numbers(num, header):
    nums = [header]
    for i in tqdm(random.normal(0, 1, num)):
        nums.append(i)
    return nums


def create_texts(num, header):
    fake = Faker()
    texts = [header]
    for _ in tqdm(range(num)):
        texts.append(f"'{fake.text(max_nb_chars=max)}'")
    return texts


def inserts(filepath: str, table: str, db_setting):
    import pandas as pd

    from sqlalchemy import create_engine, URL

    pg_url = URL.create(
        "postgresql+psycopg2",
        username=db_setting["user"],
        password=db_setting["pass"],
        host=db_setting["host"],
        port=db_setting["port"],
        database=db_setting["name"],
    )
    engine = create_engine(pg_url)

    df = pd.read_csv(filepath, delimiter=",", quotechar="'")
    df.to_sql(table, con=engine, if_exists="append")
    print(df)
    print(f"upload to {'db'} {table}")
