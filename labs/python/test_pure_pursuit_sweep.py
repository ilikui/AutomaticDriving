"""Tests for Pure Pursuit lookahead evaluation sweep."""
import unittest

from pure_pursuit_sweep import run_sweep, simulate_tracking


class PurePursuitSweepTests(unittest.TestCase):
    def test_simulation_returns_finite_metrics(self):
        metrics = simulate_tracking(6.0, adaptive=False, steps=80)
        self.assertGreater(metrics["samples"], 0)
        self.assertTrue(all(value == value for value in metrics.values()))
        self.assertGreaterEqual(metrics["max_error_m"], 0.0)

    def test_adaptive_and_fixed_modes_are_reported(self):
        results = run_sweep()
        self.assertEqual(len(results), 6)
        self.assertEqual({speed for speed, _, _ in results}, {4.0, 8.0, 12.0})
        self.assertEqual({adaptive for _, adaptive, _ in results}, {False, True})

    def test_rejects_invalid_speed(self):
        with self.assertRaises(ValueError):
            simulate_tracking(0.0, adaptive=True)

    def test_rejects_invalid_lookahead_gain(self):
        with self.assertRaises(ValueError):
            simulate_tracking(5.0, adaptive=True, lookahead_gain_s=-0.1)


if __name__ == "__main__":
    unittest.main()
