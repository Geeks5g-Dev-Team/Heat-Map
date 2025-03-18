import math


def meters_to_miles(meters):

    return 1609344 * meters


def km_to_miles(km):

    return km * 0.62137119


def miles_to_km(miles):
    return miles * 1.609344


def modify_coordinates(lat, lng, accuracy_km):
    lat_offset = lat + (accuracy_km / 111.0)

    lng_offset = lng + (accuracy_km / (111.0 * math.cos(math.radians(lat))))

    return lat_offset, lng_offset
