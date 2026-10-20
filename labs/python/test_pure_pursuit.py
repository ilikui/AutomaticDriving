"""Unit tests for the Pure Pursuit geometry example."""
import math
import unittest

from pure_pursuit import (
    pure_pursuit_steering,
    select_lookahead_target,
    simulate_straight_path,
)


class PurePursuitTests(unittest.TestCase):
    def test_straight_ahead_target_needs_no_steering(self):
        angle = pure_pursuit_steering(0, 0, 0, (5, 0), 2.7)
        self.assertAlmostEqual(angle, 0.0)

    def test_target_to_left_produces_positive_steering(self):
        angle = pure_pursuit_steering(0, 0, 0, (4, 2), 2.7)
        self.assertGreater(angle, 0.0)

    def test_target_is_transformed_relative_to_yaw(self):
        angle = pure_pursuit_steering(0, 0, math.pi / 2, (0, 5), 2.7)
        self.assertAlmostEqual(angle, 0.0, places=7)

    def test_selects_first_point_at_lookahead_distance(self):
        path = [(1, 0), (2, 0), (3, 0)]
        self.assertEqual(select_lookahead_target(path, (0, 0), 2), (2, 0))

    def test_returns_none_when_path_is_too_short(self):
        self.assertIsNone(select_lookahead_target([(1, 0)], (0, 0), 2))

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            pure_pursuit_steering(0, 0, 0, (0, 0), 2.7)
        with self.assertRaises(ValueError):
            select_lookahead_target([], (0, 0), 0)

    def test_simulation_returns_finite_pose(self):
        pose = simulate_straight_path()
        self.assertTrue(all(math.isfinite(value) for value in pose))


if __name__ == "__main__":
    unittest.main()
