"""
Utility functions.

Copyright 2024, Aqua Predict GmbH
All rights reserved
"""

import numpy as np

lat_greatest_lb = 18
lat_least_ub = 54
lon_greatest_lb = 73
lon_least_ub = 135
region_box = [
    {'lat': lat_greatest_lb, 'lon': lon_greatest_lb},
    {'lat': lat_greatest_lb, 'lon': lon_least_ub},
    {'lat': lat_least_ub, 'lon': lon_least_ub},
    {'lat': lat_least_ub, 'lon': lon_greatest_lb}
]


def generate_mockup_gw_values_and_locs(
        series_length: int,
        num_locations: int
) -> (tuple[tuple[float]], tuple[dict]):
    """

    Generate mockup data.

    Args:
        series_length:
        num_locations:

    Returns:

    """

    groundwater_bounds = (1, 10)  # arbitrary values for mockup groundwater
    # data

    groundwater_values = [None] * series_length
    for i in range(series_length):
        groundwater_values[i] = tuple(generate_mockup_values(
            num_values=num_locations, bounds=groundwater_bounds
        ))
    groundwater_values = tuple(groundwater_values)

    lat_bounds = (lat_greatest_lb, lat_least_ub)
    lon_bounds = (lon_greatest_lb, lon_least_ub)

    geographical_locations_lat = generate_mockup_values(
        num_values=num_locations, bounds=lat_bounds
    )

    geographical_locations_lon = generate_mockup_values(
        num_values=num_locations, bounds=lon_bounds
    )

    geographical_locations = tuple(
        zip(geographical_locations_lat, geographical_locations_lon)
    )

    keys = ['lat', 'lon']
    geographical_locations = [
        dict(zip(keys, item)) for item in geographical_locations
    ]

    return groundwater_values, geographical_locations


def generate_mockup_values(
        num_values: int = 10,
        bounds: tuple = (0, 10)
) -> list:
    """

    Args:
        num_values:
        bounds:

    Returns:

    """
    return np.random.uniform(bounds[0], bounds[1], num_values).tolist()


def print_mockup_data(
        groundwater_values_series: tuple[tuple[float]],
        geographical_locations: tuple[dict]
):
    """

    Args:
        groundwater_values_series (tuple[tuple[float]]):
        geographical_locations (tuple[dict]):

    Returns:

    """
    print('\n\n ----- Mockup data generated ----- ')
    print('\nMockup geographical locations:')
    for g in geographical_locations:
        print('\tlatitude: {:.2f}, longitude: {:.2f}'.format(
            g['lat'], g['lon'])
        )

    if len(groundwater_values_series) == 1:
        tmp = [round(v, 2) for v in groundwater_values_series[0]]
        print('\nSingle set of mockup groundwater values: {}'.format(tmp))
    else:
        print('\nSeries of {} sets of mockup groundwater values: '
              ''.format(len(groundwater_values_series)))
        for c, gwvs in enumerate(groundwater_values_series):
            tmp = [round(v, 2) for v in gwvs]
            print('\tSet {}: {}'.format(c+1, tmp))


def pretty_print_dict(d, indent_steps=1, indent_unit='  ',
                      logger_fun=None):
    """Print dictionary."""
    for key, value in d.items():
        if isinstance(value, dict):
            text = indent_unit * indent_steps + str(key) + ': '
            if logger_fun is None:
                print(text)
            else:
                logger_fun(text)
            pretty_print_dict(value, indent_steps + 1)
        else:
            text = indent_unit * indent_steps + str(key) + ': ' + str(value)
            if logger_fun is None:
                print(text)
            else:
                logger_fun(text)


def filter_2D_points_inside_polygon(
    points: list[dict],
    polygon: list[dict]
) -> list:
    """

    Args:
        points (list[dict]): list of the point ti be checked.
        polygon (list[dict]): list of the polygon vertexes.

    Returns:
        list: Boolean mask.
    """
    Boolean_mask = [False] * len(points)
    for i, point in enumerate(points):
        Boolean_mask[i] = is_point_in_polygon(point, polygon)

    return Boolean_mask


def is_point_in_polygon(
        point: dict,
        polygon: list[dict]
) -> bool:
    """
    Check whether the input point is inside the input polygon.

    The method implemented is described here:
    https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/

    Args:
        point (dict):
        polygon (list[dict]):

    Returns:
        Boolean: flag. True if point in polygon. False, otherwise.
    """
    num_vertices = len(polygon)
    x, y = point['lat'], point['lon']
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1['lon'], p2['lon']):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1['lon'], p2['lon']):
                # Check if the point is to the left of the maximum x coordinate
                # of the edge
                if x <= max(p1['lat'], p2['lat']):
                    # Calculate the x-intersection of the line connecting the
                    # point to the edge
                    x_intersection = (y - p1['lon']) * (p2['lat'] - p1[
                        'lat']) / (p2['lon'] - p1['lon']) + p1['lat']

                    # Check if the point is on the same line as the edge or to
                    # the left of the x-intersection
                    if p1['lat'] == p2['lat'] or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    # Return the value of the inside flag
    return inside


def set_epsilon(privacy_level: str):
    """
    Define epsilon based on the desired privacy level.

        1) epsilon in [0.01, 0.1) (very_high)
        2) epsilon in [0.1, 0.25) (high)
        3) epsilon in [0.25, 0.50) (moderate)
        4) epsilon in [0.50, 0.75) (low)
        5) epsilon in [0.75, 1.0) (very_low)

    Args:
        privacy_level (str): select the desired privacy level.
            Options:
                1) very_high
                2) high
                3) moderate
                4) low
                5) very_low
            Higher (lower) privacy level yields lower (larger) utility.

    Returns:
        float: epsilon value
    """

    if privacy_level.lower() == "very_high".lower():
        epsilon = round(np.random.uniform(0.01, 0.1), 2)
    if privacy_level.lower() == "high".lower():
        epsilon = round(np.random.uniform(0.1, 0.25), 2)
    if privacy_level.lower() == "moderate".lower():
        epsilon = round(np.random.uniform(0.25, 0.5), 2)
    if privacy_level.lower() == "low".lower():
        epsilon = round(np.random.uniform(0.5, 0.75), 2)
    if privacy_level.lower() == "very_low".lower():
        epsilon = round(np.random.uniform(0.75, 1.0), 2)

    return epsilon
