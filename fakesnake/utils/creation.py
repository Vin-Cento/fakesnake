from geopy import Point
from geopy.distance import distance
from shapely.geometry import Polygon


def create_square(lat, lon, edge_length):
    center = Point(lat, lon)
    north = distance(miles=edge_length).destination(center, 45)
    east = distance(miles=edge_length).destination(center, 135)
    south = distance(miles=edge_length).destination(center, 225)
    west = distance(miles=edge_length).destination(center, 315)

    square_points = [north, east, south, west]
    polygon = Polygon([(p.longitude, p.latitude) for p in square_points])

    return polygon
