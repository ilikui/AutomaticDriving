"""Tests for sensor timestamp gating and correlated-noise fusion."""
import unittest

from sensor_fusion_timing_covariance import (
    fuse_correlated_pair,
    require_time_alignment,
)


class TimingAndCovarianceTests(unittest.TestCase):
    def test_accepts_measurements_within_skew_limit(self):
        result = require_time_alignment([(1.0, 1.0, 2.0), (1.2, 2.0, 2.02)], 0.03)
        self.assertEqual(result, [(1.0, 1.0), (1.2, 2.0)])

    def test_rejects_stale_measurements(self):
        with self.assertRaises(ValueError):
            require_time_alignment([(1.0, 1.0, 2.0), (1.2, 2.0, 2.1)], 0.03)

    def test_rejects_invalid_timestamps_and_variances(self):
        with self.assertRaises(ValueError):
            require_time_alignment([(1.0, 1.0, float("nan"))], 0.1)
        with self.assertRaises(ValueError):
            require_time_alignment([(1.0, 0.0, 1.0)], 0.1)

    def test_independent_equal_variance_matches_weighted_average(self):
        estimate, variance = fuse_correlated_pair(10.0, 4.0, 14.0, 4.0, 0.0)
        self.assertAlmostEqual(estimate, 12.0)
        self.assertAlmostEqual(variance, 2.0)

    def test_positive_correlation_reduces_information_gain(self):
        _, independent_variance = fuse_correlated_pair(10.0, 4.0, 14.0, 4.0, 0.0)
        _, correlated_variance = fuse_correlated_pair(10.0, 4.0, 14.0, 4.0, 2.0)
        self.assertGreater(correlated_variance, independent_variance)

    def test_rejects_invalid_covariance(self):
        with self.assertRaises(ValueError):
            fuse_correlated_pair(1.0, 1.0, 2.0, 1.0, 2.0)

    def test_rejects_perfectly_redundant_pair(self):
        with self.assertRaises(ValueError):
            fuse_correlated_pair(1.0, 1.0, 2.0, 1.0, 1.0)


if __name__ == "__main__":
    unittest.main()
