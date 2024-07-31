"""
Convenience methods for safely providing input data to the Water Intelligence
platform.

Copyright 2024, Aqua Predict GmbH
All rights reserved
"""

import numpy as np

from .dp_estimator import PrivacyPreservingEstimator
from .utils import region_box, filter_2D_points_inside_polygon


class PrivacyPreservingEstimatorForRegion:
    """

    Compute differentiallly-private summary statistics for a series of
    groundwater value sets. Each groundwater value is associated with a
    geographical location belonging to a certain geographical region.
    The geographical region is defined by a polygon. Each vertex of the
    polygon is identified by a (latitude, longitude) pair.

    Args:
        groundwater_values_series (tuple[tuple[float]]): series of groundwater
            value sets for the locations. A single groundwater value for each
            location.
        locs (tuple[dict]): list of locations. Each location is a
            dictionary with 'lat', 'lon' keys containing the 'latitude' and
            the 'longitude' values for the location, respectively.
        groundwater_bounds (tuple): ('lower', 'upper') values pair containing
            the lower and upper groundwater bounds, respectively,
            for estimating the sensitivity of the differentially-private
            mean function. Default: None.
        lat_bounds (tuple): ('lower', 'upper') values pair containing
            the lower and upper latitude bounds, respectively,
            for estimating the sensitivity of the differentially-private
            mean function. Default: None.
        lon_bounds (tuple): ('lower', 'upper') values pair containing
            the lower and upper longitude bounds, respectively,
            for estimating the sensitivity of the differentially-private
            mean function. Default: None.
        privacy_budget (float): privacy budget for safely estimating
            statistics on a certain dataset.
        region_boundary (tuple[dict]): polygon identifying the region of
            interest. The default value is a box. However, polygons with an
            arbitrary number of vertexes can be used.
    """
    def __init__(
            self,
            groundwater_values_series: list[list[float]],
            locs: list[dict],
            groundwater_bounds: tuple = None,
            lat_bounds: tuple = None,
            lon_bounds: tuple = None,
            privacy_budget: float = 1.0,
            region_boundary: tuple[dict] = region_box
    ):

        self.groundwater_bounds = groundwater_bounds
        self.lat_bounds = lat_bounds
        self.lon_bounds = lon_bounds
        self.region_boundary = region_boundary

        self.groundwater_values_series, self.locs = self._filter_locations(
            locs,
            groundwater_values_series
        )

        self.dp_estimator = PrivacyPreservingEstimator(
            self.groundwater_values_series,
            self.locs,
            self.groundwater_bounds,
            self.lat_bounds,
            self.lon_bounds,
            privacy_budget
        )

    def _filter_locations(
        self,
        locs: list[dict],
        groundwater_values_series: list[list[float]]
    ):

        Boolean_mask = filter_2D_points_inside_polygon(
            locs,
            list(self.region_boundary)
        )

        # filter a list with a Boolean mask
        filtered_locs = np.array(locs)[Boolean_mask].tolist()

        diff = len(locs) - len(filtered_locs)
        if diff > 0:
            print('\n{} geographical locations ignored because they are '
                  'out of the region of interest'.format(diff))

        print('\nNumber of locations inside the region of interest: '
              '{}'.format(len(filtered_locs)))

        filtered_groundwater_values_series = [None] * len(groundwater_values_series)
        for i, groundwater_values in enumerate(groundwater_values_series):
            filtered_groundwater_values_series[i] = (
                # filter a list with a Boolean mask
                [v for b, v in zip(Boolean_mask, groundwater_values) if b]
            )

        return filtered_groundwater_values_series, filtered_locs

    def safely_estimate_mean_gw_series_for_region(
        self,
        epsilon: float = .5
    ):
        """

        Compute the differentially-private mean of the groundwater
        values. Each value is associated with a geographical location,
        identified by a (latitude, longitude) pair of values. The
        differentially private centroid of the locations is also computed.

        Args:
            epsilon (float): value for the epsilon parameter of
                Differential Privacy.

        Returns:
            float: differentially-private mean of the groundwater values
                provided.
            float: differentially-private centroid of the input locations.
        """

        dp_gw_mean_series, dp_centroid = self.dp_estimator.safely_estimate_mean_gw_series_for_locations(
            epsilon)

        return dp_gw_mean_series, dp_centroid

    def print_gw_privacy_accountant_status(self):
        """
        Convenience method.

        """
        self.dp_estimator.print_gw_privacy_accountant_status()
