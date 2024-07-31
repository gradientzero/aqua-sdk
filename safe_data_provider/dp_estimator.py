"""
Convenience methods for safely providing input data to the Water Intelligence
platform.

Copyright 2024, Aqua Predict GmbH
All rights reserved
"""

import diffprivlib as dp


class PrivacyPreservingEstimator:
    """

    Compute differentiallly-private summary statistics for a series of
    groundwater value sets. Each groundwater value is associated with a
    geographical location.

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
    """
    def __init__(
            self,
            groundwater_values_series: tuple[tuple[float]],
            locs: tuple[dict],
            groundwater_bounds: tuple = None,
            lat_bounds: tuple = None,
            lon_bounds: tuple = None,
            privacy_budget: float = 1.0
    ):
        self.groundwater_values_series = groundwater_values_series
        self.locs = locs
        self.lat_values = [loc['lat'] for loc in self.locs]
        self.lon_values = [loc['lon'] for loc in self.locs]
        self.groundwater_bounds = groundwater_bounds
        self.lat_bounds = lat_bounds
        self.lon_bounds = lon_bounds
        self.gw_privacy_accountant = dp.BudgetAccountant(privacy_budget, 0)
        self.lon_privacy_accountant = dp.BudgetAccountant(privacy_budget, 0)
        self.lat_privacy_accountant = dp.BudgetAccountant(privacy_budget, 0)
        # self.privacy_accountant.set_default()  # Using set_default(),
        # an accountant is used by default in all diffprivlib functions.

    @staticmethod
    def print_privacy_accountant_status(
            privacy_accountant: dp.BudgetAccountant
    ):
        """
        Privacy budget status.

        Args:
            privacy_accountant (dp.BudgetAccountant): Privacy accountant
                instance.
        """
        print('\nPrivacy budget status:')
        t_epsilon, t_delta = privacy_accountant.total()
        print('\tbudget spent: {:.2f}'.format(t_epsilon))
        r_epsilon, r_delta = privacy_accountant.remaining()
        print('\tbudget remaning: {:.1f}'.format(r_epsilon))

    def print_gw_privacy_accountant_status(self):
        """
        Convenience method.

        """
        self.print_privacy_accountant_status(self.gw_privacy_accountant)

    def safely_estimate_mean_gw_series_for_locations(
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
        dp_gw_mean_series = [None] * len(self.groundwater_values_series)
        for i, groundwater_values in enumerate(self.groundwater_values_series):
            dp_gw_mean_series[i] = dp.tools.mean(
                groundwater_values,
                bounds=self.groundwater_bounds,
                epsilon=epsilon,
                accountant=self.gw_privacy_accountant)

        dp_lat = dp.tools.mean(
            self.lat_values,
            bounds=self.lat_bounds,
            epsilon=epsilon,
            accountant=self.lat_privacy_accountant)

        dp_lon = dp.tools.mean(
            self.lon_values,
            bounds=self.lon_bounds,
            epsilon=epsilon,
            accountant=self.lon_privacy_accountant)

        dp_centroid = (dp_lat, dp_lon)

        # self.print_privacy_accountant_status(self.gw_privacy_accountant)

        return dp_gw_mean_series, dp_centroid
