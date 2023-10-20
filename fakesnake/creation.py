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


def create_shapes(num, dist):
    fake = Faker()
    fake.add_provider(geo)
    polygons = []

    for _ in tqdm(range(num)):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        # polygons.append(square_polygon)
        polygons.append(square_polygon.__str__().replace("\n", ""))
    return polygons


def create_names(num):
    fake = Faker()
    names = []
    for _ in tqdm(range(num)):
        names.append(fake.name())
    return names


def create_emails(num):
    fake = Faker()
    emails = []
    for _ in tqdm(range(num)):
        emails.append(fake.email())
    return emails


def create_addresses(num):
    fake = Faker()
    addresses = []
    for _ in tqdm(range(num)):
        street_address = fake.street_address()
        # Generate a random city
        city = fake.city()
        # Generate a random state
        state = fake.state()
        # Generate a random postal code
        postal_code = fake.postcode()
        # Combine the parts to create an address
        addresses.append(f"{street_address}, {city}, {state} {postal_code}")
    return addresses


def create_passwords(num, min, max):
    assert min > 3, "min should be greater than 3"
    assert (
        max >= min
    ), "max should be greater than or equal to min, (default for max is 25)"

    fake = Faker()
    passwords = []

    for _ in tqdm(range(num)):
        passwords.append(
            fake.password(
                length=randint(min, max),
            )
        )
    return passwords


def create_numbers(num):
    nums = []
    for i in tqdm(random.normal(0, 1, num)):
        nums.append(i)
    return nums
