"""2D homogeneous coordinate transform helpers for learning.

Convention: T_parent_child maps coordinates expressed in child frame into
parent frame: p_parent = T_parent_child @ p_child.
Angles are radians; distances use one consistent unit.
"""
from __future__ import annotations

import math
from typing import Sequence, Tuple

Matrix3 = Tuple[Tuple[float, float, float], ...]
Point2 = Tuple[float, float]


def transform_2d(x: float, y: float, yaw_rad: float) -> Matrix3:
    """Return a 3x3 transform from a local frame to its parent frame."""
    if not all(math.isfinite(value) for value in (x, y, yaw_rad)):
        raise ValueError("transform parameters must be finite")
    c = math.cos(yaw_rad)
    s = math.sin(yaw_rad)
    return (
        (c, -s, x),
        (s, c, y),
        (0.0, 0.0, 1.0),
    )


def multiply_3x3(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> Matrix3:
    """Multiply two 3x3 matrices."""
    if len(a) != 3 or len(b) != 3 or any(len(row) != 3 for row in a) or any(len(row) != 3 for row in b):
        raise ValueError("both matrices must be 3x3")
    return tuple(
        tuple(sum(float(a[i][k]) * float(b[k][j]) for k in range(3)) for j in range(3))
        for i in range(3)
    )


def apply_transform(matrix: Sequence[Sequence[float]], point: Point2) -> Point2:
    """Transform a 2D point using a homogeneous 3x3 matrix."""
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("matrix must be 3x3")
    x, y = point
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("point coordinates must be finite")
    px = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    py = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    pw = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2]
    if not math.isfinite(pw) or abs(pw) < 1e-12:
        raise ValueError("invalid homogeneous coordinate")
    return px / pw, py / pw


def inverse_rigid_2d(matrix: Sequence[Sequence[float]]) -> Matrix3:
    """Invert a rigid 2D transform (rotation + translation, no scale/shear)."""
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("matrix must be 3x3")
    r00, r01, tx = matrix[0]
    r10, r11, ty = matrix[1]
    if any(abs(value - expected) > 1e-8 for value, expected in (
        (matrix[2][0], 0.0), (matrix[2][1], 0.0), (matrix[2][2], 1.0)
    )):
        raise ValueError("matrix must be a rigid homogeneous transform")
    # A valid 2D rotation has orthonormal columns and determinant +1.
    if (abs(r00*r00 + r10*r10 - 1.0) > 1e-6
        or abs(r01*r01 + r11*r11 - 1.0) > 1e-6
        or abs(r00*r01 + r10*r11) > 1e-6
        or abs(r00*r11 - r01*r10 - 1.0) > 1e-6):
        raise ValueError("rotation component is not orthonormal")
    return (
        (r00, r10, -(r00 * tx + r10 * ty)),
        (r01, r11, -(r01 * tx + r11 * ty)),
        (0.0, 0.0, 1.0),
    )


def main() -> None:
    # Example: sensor frame is translated 2 m forward and rotated 90 degrees
    # counter-clockwise relative to the vehicle frame.
    vehicle_from_sensor = transform_2d(2.0, 0.0, math.pi / 2.0)
    point_sensor = (1.0, 0.0)
    point_vehicle = apply_transform(vehicle_from_sensor, point_sensor)
    point_sensor_round_trip = apply_transform(inverse_rigid_2d(vehicle_from_sensor), point_vehicle)
    print(f"point in sensor frame:  {point_sensor}")
    print(f"point in vehicle frame: ({point_vehicle[0]:.3f}, {point_vehicle[1]:.3f})")
    print(f"inverse transform:      ({point_sensor_round_trip[0]:.3f}, {point_sensor_round_trip[1]:.3f})")


if __name__ == "__main__":
    main()
