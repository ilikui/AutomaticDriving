"""Tests for 2D homogeneous coordinate transforms."""
import math
import unittest

from coordinate_transform_2d import (
    apply_transform,
    inverse_rigid_2d,
    multiply_3x3,
    transform_2d,
)


class CoordinateTransformTests(unittest.TestCase):
    def assertPointAlmostEqual(self, actual, expected, places=7):
        self.assertAlmostEqual(actual[0], expected[0], places=places)
        self.assertAlmostEqual(actual[1], expected[1], places=places)

    def test_translation_only(self):
        self.assertPointAlmostEqual(apply_transform(transform_2d(2, -3, 0), (1, 4)), (3, 1))

    def test_ninety_degree_rotation_and_translation(self):
        matrix = transform_2d(2, 0, math.pi / 2)
        self.assertPointAlmostEqual(apply_transform(matrix, (1, 0)), (2, 1))

    def test_inverse_round_trip(self):
        matrix = transform_2d(1.2, -4.5, 0.7)
        point = (3.4, -1.1)
        self.assertPointAlmostEqual(apply_transform(inverse_rigid_2d(matrix), apply_transform(matrix, point)), point)

    def test_matrix_composition(self):
        parent_from_child = transform_2d(1, 0, math.pi / 2)
        child_from_sensor = transform_2d(2, 0, 0)
        composed = multiply_3x3(parent_from_child, child_from_sensor)
        self.assertPointAlmostEqual(apply_transform(composed, (0, 0)), (1, 2))

    def test_rejects_non_finite_transform(self):
        with self.assertRaises(ValueError):
            transform_2d(float("nan"), 0, 0)

    def test_rejects_non_rigid_inverse(self):
        with self.assertRaises(ValueError):
            inverse_rigid_2d(((2, 0, 0), (0, 2, 0), (0, 0, 1)))


if __name__ == "__main__":
    unittest.main()
