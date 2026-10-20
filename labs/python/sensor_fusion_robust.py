"""Robust scalar fusion with median/MAD outlier screening.

This is an educational gate, not a production multi-object fusion pipeline.
Inputs must already describe the same quantity in the same coordinate frame.
"""
from __future__ import annotations

import math
from typing import List, Tuple

Measurement = Tuple[float, float]  # (value, variance)


def robust_weighted_fuse(
    measurements: List[Measurement],
    threshold_sigma: float = 3.0,
) -> Tuple[float, float, List[int]]:
    """Return (estimate, variance, accepted input indices).

    A median/MAD gate removes gross outliers before inverse-variance fusion.
    The gate threshold also respects each measurement's stated standard
    deviation. With very small samples, robust statistics are inherently weak.
    """
    if not measurements:
        raise ValueError("at least one measurement is required")
    if not math.isfinite(threshold_sigma) or threshold_sigma <= 0:
        raise ValueError("threshold_sigma must be finite and positive")
    for value, variance in measurements:
        if not math.isfinite(value) or not math.isfinite(variance) or variance <= 0:
            raise ValueError("values must be finite and variances positive")

    values = [value for value, _ in measurements]
    ordered = sorted(values)
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) / 2.0
    )
    deviations = sorted(abs(value - median) for value in values)
    mad = (
        deviations[middle]
        if len(deviations) % 2
        else (deviations[middle - 1] + deviations[middle]) / 2.0
    )
    robust_sigma = 1.4826 * mad

    accepted = [
        index
        for index, (value, variance) in enumerate(measurements)
        if abs(value - median)
        <= threshold_sigma * max(robust_sigma, math.sqrt(variance))
    ]
    if not accepted:  # Defensive fallback; the median itself should normally pass.
        accepted = [min(range(len(values)), key=lambda i: abs(values[i] - median))]

    information = sum(1.0 / measurements[i][1] for i in accepted)
    estimate = sum(
        measurements[i][0] / measurements[i][1] for i in accepted
    ) / information
    return estimate, 1.0 / information, accepted


def main() -> None:
    measurements = [(10.1, 0.25), (9.8, 0.36), (10.0, 0.16), (42.0, 0.25)]
    estimate, variance, accepted = robust_weighted_fuse(measurements)
    rejected = [i for i in range(len(measurements)) if i not in accepted]
    print("Robust scalar fusion demo (synthetic, meters)")
    print(f"accepted measurement indices: {accepted}")
    print(f"rejected measurement indices: {rejected}")
    print(f"fused estimate: {estimate:.3f} m")
    print(f"reported variance: {variance:.4f} m^2")


if __name__ == "__main__":
    main()
