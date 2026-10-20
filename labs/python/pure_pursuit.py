"""Geometric Pure Pursuit controller example for an offline kinematic model.

Coordinates: world x forward at yaw=0, world y left, yaw positive counter-clockwise.
This is a teaching example, not a safety-qualified vehicle controller.
"""
from __future__ import annotations

import math
from typing import Iterable, Optional, Sequence, Tuple

Point2 = Tuple[float, float]


def select_lookahead_target(
    path: Sequence[Point2], position: Point2, lookahead_m: float
) -> Optional[Point2]:
    """Return the first path point at least lookahead_m from position."""
    if not math.isfinite(lookahead_m) or lookahead_m <= 0:
        raise ValueError("lookahead_m must be finite and greater than zero")
    px, py = position
    if not math.isfinite(px) or not math.isfinite(py):
        raise ValueError("position must be finite")
    for point in path:
        if len(point) != 2 or not all(math.isfinite(v) for v in point):
            raise ValueError("path points must contain two finite coordinates")
        if math.hypot(point[0] - px, point[1] - py) >= lookahead_m:
            return point
    return None


def pure_pursuit_steering(
    vehicle_x: float,
    vehicle_y: float,
    yaw_rad: float,
    target: Point2,
    wheelbase_m: float,
) -> float:
    """Compute front-wheel steering angle in radians from a target point."""
    values = (vehicle_x, vehicle_y, yaw_rad, target[0], target[1], wheelbase_m)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("inputs must be finite")
    if wheelbase_m <= 0:
        raise ValueError("wheelbase_m must be greater than zero")

    dx = target[0] - vehicle_x
    dy = target[1] - vehicle_y
    # Transform target into vehicle coordinates.
    local_x = math.cos(yaw_rad) * dx + math.sin(yaw_rad) * dy
    local_y = -math.sin(yaw_rad) * dx + math.cos(yaw_rad) * dy
    distance_sq = local_x * local_x + local_y * local_y
    if distance_sq < 1e-12:
        raise ValueError("target must not coincide with vehicle position")
    curvature = 2.0 * local_y / distance_sq
    return math.atan(wheelbase_m * curvature)


def simulate_straight_path(steps: int = 20, dt_s: float = 0.1) -> Tuple[float, float, float]:
    """Follow a straight path with a simple bicycle-model kinematic update."""
    if steps < 1 or not math.isfinite(dt_s) or dt_s <= 0:
        raise ValueError("steps and dt_s must be positive")
    wheelbase = 2.7
    speed = 4.0
    x, y, yaw = 0.0, 0.8, 0.0
    path = [(i * 0.5, 0.0) for i in range(1, 101)]
    for _ in range(steps):
        target = select_lookahead_target(path, (x, y), 2.0)
        if target is None:
            break
        steering = pure_pursuit_steering(x, y, yaw, target, wheelbase)
        x += speed * math.cos(yaw) * dt_s
        y += speed * math.sin(yaw) * dt_s
        yaw += speed / wheelbase * math.tan(steering) * dt_s
    return x, y, yaw


def main() -> None:
    x, y, yaw = simulate_straight_path()
    print("Pure Pursuit kinematic demonstration (offline only)")
    print(f"final pose: x={x:.3f} m, y={y:.3f} m, yaw={math.degrees(yaw):.2f} deg")


if __name__ == "__main__":
    main()
