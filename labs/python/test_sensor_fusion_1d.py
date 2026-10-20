"""Tests for inverse-variance scalar sensor fusion."""
import unittest

from sensor_fusion_1d import run_demo, weighted_fuse


class SensorFusionTests(unittest.TestCase):
    def test_equal_variance_is_arithmetic_mean(self):
        estimate, variance = weighted_fuse([(10.0, 4.0), (14.0, 4.0)])
        self.assertAlmostEqual(estimate, 12.0)
        self.assertAlmostEqual(variance, 2.0)

    def test_lower_variance_measurement_has_more_weight(self):
        estimate, _ = weighted_fuse([(0.0, 100.0), (10.0, 1.0)])
        self.assertGreater(estimate, 9.0)

    def test_rejects_empty_or_invalid_measurements(self):
        with self.assertRaises(ValueError):
            weighted_fuse([])
        with self.assertRaises(ValueError):
            weighted_fuse([(1.0, 0.0)])
        with self.assertRaises(ValueError):
            weighted_fuse([(float("nan"), 1.0)])

    def test_demo_is_reproducible(self):
        self.assertEqual(run_demo(), run_demo())

    def test_demo_returns_requested_sample_count(self):
        self.assertEqual(len(run_demo(samples=12)), 12)


if __name__ == "__main__":
    unittest.main()
