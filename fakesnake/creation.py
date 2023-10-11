from geopy import Point
from geopy.distance import distance
from shapely.geometry import Polygon

from faker import Faker
from faker.providers import geo

from numpy import random


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

    for _ in range(num):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        polygons.append(square_polygon)
        print(square_polygon.__str__().replace("\n", ""))


def create_names(num):
    fake = Faker()
    for _ in range(num):
        print(fake.name())


def create_emails(num):
    fake = Faker()
    for _ in range(num):
        print(fake.email())


def create_addresses(num):
    fake = Faker()
    for _ in range(num):
        street_address = fake.street_address()
        # Generate a random city
        city = fake.city()
        # Generate a random state
        state = fake.state()
        # Generate a random postal code
        postal_code = fake.postcode()
        # Combine the parts to create an address
        print(f"{street_address}, {city}, {state} {postal_code}")


def create_passwords(num):
    fake = Faker()
    for _ in range(num):
        print(
            fake.password(
                length=12,
            )
        )


def create_numbers(num):
    for i in random.normal(0, 1, num):
        print(i)
