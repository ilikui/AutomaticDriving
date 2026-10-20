"""Unit tests for the educational 1D Kalman filter."""
import math
import unittest

from kalman_1d import ConstantVelocityKalman, run_demo


class ConstantVelocityKalmanTests(unittest.TestCase):
    def test_predict_advances_constant_velocity(self):
        kalman = ConstantVelocityKalman(initial_position_m=2, initial_velocity_mps=3)
        position, velocity = kalman.predict(0.5)
        self.assertAlmostEqual(position, 3.5)
        self.assertAlmostEqual(velocity, 3.0)

    def test_update_moves_position_toward_measurement(self):
        kalman = ConstantVelocityKalman(initial_position_m=0, position_variance=1)
        before = kalman.x[0]
        position, _ = kalman.update(10)
        self.assertGreater(position, before)
        self.assertLess(position, 10)

    def test_invalid_dt_is_rejected(self):
        kalman = ConstantVelocityKalman()
        for dt in (0, -1, float("nan"), float("inf")):
            with self.subTest(dt=dt), self.assertRaises(ValueError):
                kalman.predict(dt)

    def test_invalid_measurement_is_rejected(self):
        kalman = ConstantVelocityKalman()
        with self.assertRaises(ValueError):
            kalman.update(float("nan"))

    def test_covariance_stays_symmetric_and_nonnegative_diagonal(self):
        kalman = ConstantVelocityKalman()
        for row in run_demo(steps=100):
            kalman.predict(0.5)
            kalman.update(row.measurement_m)
        self.assertAlmostEqual(kalman.p[0][1], kalman.p[1][0], places=12)
        self.assertGreaterEqual(kalman.p[0][0], 0)
        self.assertGreaterEqual(kalman.p[1][1], 0)
        self.assertTrue(all(math.isfinite(value) for state in kalman.p for value in state))

    def test_demo_is_reproducible(self):
        self.assertEqual(run_demo(), run_demo())


if __name__ == "__main__":
    unittest.main()
