"""Compare fixed and speed-adaptive lookahead in a synthetic path-following task.

Offline kinematic bicycle simulation only. This is not a vehicle-ready controller.
"""
from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from pure_pursuit import pure_pursuit_steering

Point = Tuple[float, float]


def build_sinusoidal_path(length_m: float = 100.0, step_m: float = 0.25) -> List[Point]:
    if not math.isfinite(length_m) or not math.isfinite(step_m) or length_m <= 0 or step_m <= 0:
        raise ValueError("length_m and step_m must be finite and positive")
    count = int(length_m / step_m) + 1
    return [(i * step_m, 2.0 * math.sin(i * step_m / 8.0)) for i in range(count)]


def simulate_tracking(
    speed_mps: float,
    *,
    adaptive: bool,
    base_lookahead_m: float = 2.5,
    lookahead_gain_s: float = 0.25,
    dt_s: float = 0.05,
    steps: int = 1200,
) -> Dict[str, float]:
    """Return RMSE, maximum absolute lateral error, and final position."""
    values = (speed_mps, base_lookahead_m, lookahead_gain_s, dt_s)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("numeric parameters must be finite")
    if speed_mps <= 0 or base_lookahead_m <= 0 or lookahead_gain_s < 0 or dt_s <= 0 or steps < 1:
        raise ValueError("speed, lookahead, dt and steps must be positive; gain cannot be negative")

    path = build_sinusoidal_path()
    wheelbase_m = 2.7
    x, y, yaw = 0.0, path[0][1] - 0.8, 0.0
    errors: List[float] = []
    nearest_index = 0

    for _ in range(steps):
        # Search only forward from the previous nearest point to preserve path progress.
        end = min(len(path), nearest_index + 81)
        nearest_index = min(
            range(nearest_index, end),
            key=lambda i: math.hypot(path[i][0] - x, path[i][1] - y),
        )
        px, py = path[nearest_index]
        errors.append(math.hypot(px - x, py - y))

        lookahead = (
            min(8.0, max(2.0, base_lookahead_m + lookahead_gain_s * speed_mps))
            if adaptive else base_lookahead_m
        )
        target = None
        for point in path[nearest_index:]:
            if math.hypot(point[0] - x, point[1] - y) >= lookahead:
                target = point
                break
        if target is None:
            break

        steering = pure_pursuit_steering(x, y, yaw, target, wheelbase_m)
        x += speed_mps * math.cos(yaw) * dt_s
        y += speed_mps * math.sin(yaw) * dt_s
        yaw += speed_mps / wheelbase_m * math.tan(steering) * dt_s
        yaw = math.atan2(math.sin(yaw), math.cos(yaw))

    if not errors:
        raise RuntimeError("simulation did not produce tracking samples")
    return {
        "rmse_m": math.sqrt(sum(e * e for e in errors) / len(errors)),
        "max_error_m": max(errors),
        "samples": float(len(errors)),
        "final_x_m": x,
        "final_y_m": y,
    }


def run_sweep() -> List[Tuple[float, bool, Dict[str, float]]]:
    results = []
    for speed in (4.0, 8.0, 12.0):
        for adaptive in (False, True):
            results.append((speed, adaptive, simulate_tracking(speed, adaptive=adaptive)))
    return results


def main() -> None:
    print("Pure Pursuit lookahead sweep (synthetic sinusoidal path)")
    print("speed_mps  mode      rmse_m  max_error_m  samples")
    for speed, adaptive, metrics in run_sweep():
        mode = "adaptive" if adaptive else "fixed"
        print(f"{speed:9.1f}  {mode:8s}  {metrics['rmse_m']:6.3f}  "
              f"{metrics['max_error_m']:11.3f}  {int(metrics['samples']):7d}")
    print("Compare trends, not just one score: this model omits tire dynamics, actuator delay and limits.")


if __name__ == "__main__":
    main()
