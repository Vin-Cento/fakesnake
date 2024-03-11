from faker import Faker
from faker.providers import geo

from numpy import random

from random import randint
from typing import List
from geojson import Feature, FeatureCollection, dumps
from shapely.geometry import mapping

from ..utils.util import create_square


def create_shapes(num, dist, header=None) -> List[str]:
    fake = Faker()
    fake.add_provider(geo)
    polygons = [header] if header else []
    for _ in range(num):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        polygons.append(square_polygon.__str__().replace("\n", ""))
    return polygons


def create_points(num, header=None) -> List[str]:
    fake = Faker()
    fake.add_provider(geo)
    points = [header] if header else []
    for _ in range(num):
        lat, lon = fake.latlng()
        # TODO: automate the srid
        points.append(f"SRID=4326;Point({lat} {lon})")
    return points


def create_geojson(num, dist) -> List[str]:
    fake = Faker()
    fake.add_provider(geo)
    polygons = []
    for _ in range(num):
        # Generate random latitude and longitude
        lat, lon = fake.latlng()
        square_polygon = create_square(lat, lon, dist)
        polygons.append(square_polygon)

    features = []
    for polygon in polygons:
        feature = Feature(geometry=mapping(polygon), properties={})
        features.append(feature)
        feature_collection = FeatureCollection(features)
        geojson_str = dumps(feature_collection, indent=2)
    return geojson_str  # type: ignore


def create_names(num, max_nb_chars=None, with_quotes=False, header=None) -> List[str]:
    fake = Faker()
    names = [header] if header else []
    for _ in range(num):
        if with_quotes:
            if max_nb_chars:
                names.append(f"'{fake.name()[:max_nb_chars]}'")
            else:
                names.append(f"'{fake.name()}'")
        else:
            if max_nb_chars:
                names.append(fake.name()[:max_nb_chars])
            else:
                names.append(fake.name())
    return names


def create_emails(num, header=None) -> List[str]:
    fake = Faker()
    emails = [header] if header else []
    for _ in range(num):
        emails.append(f"'{fake.email()}'")
    return emails


def create_addresses(num, header=None) -> List[str]:
    fake = Faker()
    addresses = [header] if header else []
    for _ in range(num):
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

    for _ in range(num):
        passwords.append(f"'{fake.password(length=randint(min, max),)}'")
    return passwords


def create_numbers(num, header=None) -> List[str]:
    nums = [header] if header else []
    for i in random.normal(0, 1, num):
        nums.append(i)
    return nums


def create_ints(num, header=None) -> List[str]:
    ints = [header] if header else []
    for _ in range(num):
        ints.append(random.randint(-100, 100))

    return ints


def create_texts(num, max, with_quotes=False, header=None) -> List[str]:
    fake = Faker()
    texts = [header] if header else []
    for _ in range(num):
        if with_quotes:
            texts.append(f"'{fake.text(max_nb_chars=max)}'")
        else:
            texts.append(fake.text(max_nb_chars=max))
    return texts


def create_uuid(num, header=None) -> List[str]:
    fake = Faker()
    uuids = [header] if header else []
    for _ in range(num):
        uuids.append(f"'{fake.uuid4()}'")
    return uuids
