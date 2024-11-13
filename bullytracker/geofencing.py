from shapely.geometry import Polygon, Point


# Transforms location (lat and long) to a string.
# If the location lies within one of the boundaries defined
# by the school, the name of the boundary is returned
# otherwise, a google maps link to the location is returned.
def determine_location(lat, long, list_of_boundaries):
    if lat == 0.0 and long == 0.0:
        return "Location Unavailable!"

    for boundary in list_of_boundaries:
        if boundary_contains(lat, long, boundary.get("coords")):
            return boundary.get("name")

    return "https://www.google.com/maps/search/?api=1&query=" + str(lat) + "," + str(long)


# Determines if the given location determined by latitude and longitude
# Lies within a boundary represented by list of coordinates
# (last point in list of coordinates must be the same as the first)
def boundary_contains(lat, long, list_of_coordiantes):
    transformed_coordinates = []

    for coord in list_of_coordiantes:
        transformed_coordinates.append((coord.get("lat"), coord.get("long")))

    boundary = Polygon(transformed_coordinates)

    location = Point(lat, long)

    return boundary.contains(location)
