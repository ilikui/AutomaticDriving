"""A minimal scalar sensor-fusion example using inverse-variance weighting.

This illustrates fusion of independent, unbiased measurements of the same
quantity. Real sensor fusion needs association, coordinate/time alignment,
correlated-noise handling and robust outlier management.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class FusionRow:
    truth_m: float
    camera_m: float
    radar_m: float
    fused_m: float
    camera_error_m: float
    radar_error_m: float
    fused_error_m: float


def weighted_fuse(measurements: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Return (fused estimate, fused variance) for (value, variance) pairs."""
    if not measurements:
        raise ValueError("at least one measurement is required")
    if any(not math.isfinite(value) or not math.isfinite(var) or var <= 0
           for value, var in measurements):
        raise ValueError("measurements must be finite and variances positive")
    total_information = sum(1.0 / variance for _, variance in measurements)
    estimate = sum(value / variance for value, variance in measurements) / total_information
    return estimate, 1.0 / total_information


def run_demo(seed: int = 11, samples: int = 100) -> List[FusionRow]:
    if samples < 1:
        raise ValueError("samples must be at least one")
    rng = random.Random(seed)
    truth = 25.0
    camera_sigma = 2.0
    radar_sigma = 0.8
    rows = []
    for _ in range(samples):
        camera = truth + rng.gauss(0.0, camera_sigma)
        radar = truth + rng.gauss(0.0, radar_sigma)
        fused, _ = weighted_fuse([
            (camera, camera_sigma**2),
            (radar, radar_sigma**2),
        ])
        rows.append(FusionRow(
            truth, camera, radar, fused,
            camera - truth, radar - truth, fused - truth,
        ))
    return rows


def rmse(errors: List[float]) -> float:
    if not errors:
        raise ValueError("at least one error is required")
    return math.sqrt(sum(error * error for error in errors) / len(errors))


def main() -> None:
    rows = run_demo()
    print("Scalar fusion demo (synthetic measurements; meters)")
    print("sample  camera  radar  fused")
    for index, row in enumerate(rows[:10], start=1):
        print(f"{index:>6}  {row.camera_m:6.2f}  {row.radar_m:5.2f}  {row.fused_m:5.2f}")
    print("RMSE:")
    print(f"  camera: {rmse([row.camera_error_m for row in rows]):.3f} m")
    print(f"  radar:  {rmse([row.radar_error_m for row in rows]):.3f} m")
    print(f"  fused:  {rmse([row.fused_error_m for row in rows]):.3f} m")


if __name__ == "__main__":
    main()
