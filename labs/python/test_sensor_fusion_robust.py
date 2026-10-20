"""Tests for median/MAD-gated scalar sensor fusion."""
import unittest

from sensor_fusion_robust import robust_weighted_fuse


class RobustSensorFusionTests(unittest.TestCase):
    def test_rejects_a_gross_outlier(self):
        measurements = [(10.1, 0.25), (9.8, 0.36), (10.0, 0.16), (42.0, 0.25)]
        estimate, variance, accepted = robust_weighted_fuse(measurements)
        self.assertEqual(accepted, [0, 1, 2])
        self.assertAlmostEqual(estimate, 10.0, delta=0.2)
        self.assertGreater(variance, 0.0)

    def test_no_outlier_keeps_all_measurements(self):
        _, _, accepted = robust_weighted_fuse([(10.0, 1.0), (10.2, 1.0), (9.9, 1.0)])
        self.assertEqual(accepted, [0, 1, 2])

    def test_uses_lower_variance_for_more_weight_after_gating(self):
        estimate, _, accepted = robust_weighted_fuse([(0.0, 100.0), (10.0, 0.01)])
        self.assertEqual(accepted, [0, 1])
        self.assertGreater(estimate, 9.9)

    def test_rejects_invalid_arguments(self):
        for measurements in ([], [(1.0, 0.0)], [(float("nan"), 1.0)]):
            with self.subTest(measurements=measurements):
                with self.assertRaises(ValueError):
                    robust_weighted_fuse(measurements)
        with self.assertRaises(ValueError):
            robust_weighted_fuse([(1.0, 1.0)], threshold_sigma=0.0)

    def test_single_measurement_is_preserved(self):
        estimate, variance, accepted = robust_weighted_fuse([(7.0, 0.5)])
        self.assertEqual(estimate, 7.0)
        self.assertEqual(variance, 0.5)
        self.assertEqual(accepted, [0])


if __name__ == "__main__":
    unittest.main()
