"""
Some examples of usage.

Copyright 2024, Aqua Predict GmbH
All rights reserved
"""
from . import dp_estimator as dpe
from . import dp_estimator_for_region as dper
from . import utils as ut


def use_case_1(
    privacy_budget=1.0,
    groundwater_bounds: tuple = (0, 15),
    lat_bounds: tuple = None,
    lon_bounds: tuple = None,
    epsilon=.5,
    num_locations=10,
    series_length=1
):
    """
    Estimate the differentially-private mean series of the groundwater values
    for a certain set of geographical locations.

    Args:
        privacy_budget (float):
        groundwater_bounds (tuple): Default: (0, 15)
        lat_bounds (tuple): Default: None
        lon_bounds (tuple): Default: None
        epsilon (float): value for the epsilon parameter of differential
            privacy.
        num_locations (int): number of geographical locations. One groundwater value
            for each location.
        series_length (int): length of the series.

    """
    groundwater_values_series, geographical_locations = (
        ut.generate_mockup_gw_values_and_locs(
            series_length,
            num_locations
        )
    )

    ut.print_mockup_data(groundwater_values_series, geographical_locations)

    ppe = dpe.PrivacyPreservingEstimator(
        groundwater_values_series,
        geographical_locations,
        groundwater_bounds=groundwater_bounds,
        lat_bounds=lat_bounds,
        lon_bounds=lon_bounds,
        privacy_budget=privacy_budget
    )

    dp_gw_mean_series, dp_centroid = ppe.safely_estimate_mean_gw_series_for_locations(
        epsilon=epsilon)
    print_dp_results(ppe, series_length, dp_gw_mean_series, dp_centroid)


def print_dp_results(dp_es, series_length, dp_gw_mean_series,
                     dp_centroid):
    """

    Args:
        dp_es: Differentially-private mean estimator instance.
        series_length:
        dp_gw_mean_series:
        dp_centroid:

    Returns:

    """
    print('\n\n ----- Results of the computation ----- ')
    if series_length == 1:
        print(
            '\nPrivacy-preserving estimations:'
            '\n\t - Differentially-private groundwater mean: {:.1f}'.format(
                dp_gw_mean_series[0]),
            '\n\t - Differentially-private centroid of the geographical '
            'locations: ({:.2f}, {:.2f})'.format(dp_centroid[0],
                                                 dp_centroid[1])
        )
    else:
        print(
            '\nPrivacy-preserving estimations:'
            '\n\t - Differentially-private groundwater mean series: {}'.format(
                [round(float(v), 1) for v in dp_gw_mean_series]),
            '\n\t - Differentially-private centroid of the geographical '
            'locations: ({:.2f}, {:.2f})'.format(dp_centroid[0],
                                                 dp_centroid[1])
        )

    dp_es.print_gw_privacy_accountant_status()


def use_case_2(
    privacy_budget=1.0,
    groundwater_bounds: tuple = (0, 15),
    lat_bounds: tuple = None,
    lon_bounds: tuple = None,
    epsilon=.5,
    num_locations=100,
    series_length=1,
    polygon: tuple[dict] = ut.region_box
):
    """
    Estimate the differentially-private mean series of the groundwater values
    for the geographical locations inside a certain region specified by the
    input polygon.

    Args:
        privacy_budget (float):
        groundwater_bounds (tuple): Default: (0, 15)
        lat_bounds (tuple): Default: None
        lon_bounds (tuple): Default: None
        epsilon (float):
        num_locations (int): number of geographical locations. One groundwater value
            for each location.
        series_length (int): length of the series.
        polygon (tuple[dict])
    """
    groundwater_values_series, geographical_locations = (
        ut.generate_mockup_gw_values_and_locs(
            series_length,
            num_locations - 2
        )
    )

    # Add a pair of out-of-region locations
    oor_geographical_locations = (
        {'lat': 60, 'lon': 80},
        {'lat': 15, 'lon': 50},
    )
    geographical_locations += oor_geographical_locations
    groundwater_values_series = list(groundwater_values_series)
    for c in range(len(groundwater_values_series)):
        groundwater_values_series[c] += (7, 5)
    groundwater_values_series = tuple(groundwater_values_series)

    ut.print_mockup_data(groundwater_values_series, geographical_locations)

    es = dper.PrivacyPreservingEstimatorForRegion(
        groundwater_values_series,
        geographical_locations,
        groundwater_bounds,
        lat_bounds=lat_bounds,
        lon_bounds=lon_bounds,
        privacy_budget=privacy_budget,
        region_boundary=polygon
    )
    dp_gw_mean_series, dp_centroid = (
        es.safely_estimate_mean_gw_series_for_region(epsilon=epsilon)
    )
    print_dp_results(es, series_length, dp_gw_mean_series, dp_centroid)
